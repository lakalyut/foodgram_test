from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db.models import Exists, OuterRef, Value, Count, Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import generics, status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, SAFE_METHODS
from rest_framework.response import Response

from api.filters import IngredientFilter, RecipeFilter
from recipes.models import Subscribe, Recipe, Tag, Ingredient
from . import constants
from .mixins import RecipeAccessMixin
from .pagination import PagePagination
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import (
    CreateUserSerializer,
    FavoriteRecipeSerializer,
    IngredientSerializer,
    RecipeCreateUpdateSerializer,
    RecipeReadSerializer,
    RecipeShortSerializer,
    SetAvatarSerializer,
    ShoppingCartSerializer,
    SubscriptionSerializer,
    TagSerializer,
    UserSerializer,

)
from .utils import create_short_link, generate_shopping_cart_csv

User = get_user_model()


class SubscriptionView(generics.CreateAPIView, generics.DestroyAPIView):
    """Подписка и отписка от пользователя."""

    permission_classes = (IsAuthenticated,)
    serializer_class = SubscriptionSerializer

    def get_author(self):
        """Получение автора по user_id."""
        author_id = self.kwargs.get('user_id')
        return get_object_or_404(User, id=author_id)

    def create(self, request, *args, **kwargs):
        author = self.get_author()
        print(f"Пользователь {request.user} подписывается на {author}")
        if request.user.id == author.id:
            return Response(
                {'errors': constants.ERROR_SELF_SUBSCRIBE},
                status=status.HTTP_400_BAD_REQUEST
            )

        if Subscribe.objects.filter(user=request.user, author=author).exists():
            return Response(
                {'errors': constants.ERROR_ALREADY_SUBSCRIBED},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            subscription = Subscribe.objects.create(user=request.user,
                                                    author=author)
            serializer = self.get_serializer(subscription,
                                             context={'request': request})

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"Ошибка создания подписки: {e}")
            return Response({'errors': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        author = self.get_author()
        subscription = Subscribe.objects.filter(
            user=request.user, author=author
        )

        if not subscription.exists():
            return Response(
                {'errors': 'Вы не подписаны на этого пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )

        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        """Проверка автора на существования."""
        author_id = self.kwargs.get('user_id')
        author = get_object_or_404(User, id=author_id)
        return author


class CustomUserViewSet(UserViewSet):
    serializer_class = UserSerializer
    pagination_class = PagePagination

    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return User.objects.annotate(
                is_subscribed=Exists(
                    self.request.user.follower.filter(author=OuterRef('id'))
                )
            ).prefetch_related('follower', 'following')
        return User.objects.annotate(is_subscribed=Value(False))

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        if self.action == 'subscriptions':
            return SubscriptionSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password=password)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
        serializer_class=SubscriptionSerializer,
        pagination_class=PagePagination
    )
    def subscriptions(self, request):
        """Получение списка подписок текущего пользователя."""
        queryset = (
            Subscribe.objects.filter(user=request.user)
            .select_related(
                'author',
            )
            .annotate(recipes_count=Count('author__recipe'))
            .order_by('id')
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(
                page, many=True, context={'request': request}
            )
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            queryset, many=True, context={'request': request}
        )
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['put'],
        permission_classes=[IsAuthenticated],
    )
    def upload_avatar(self, request):
        """Загрузка аватара пользователя."""
        serializer = SetAvatarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.user.avatar:
            request.user.avatar.delete()

        request.user.avatar = serializer.validated_data['avatar']
        request.user.save()

        return Response(
            {'avatar': request.build_absolute_uri(request.user.avatar.url)},
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=['delete'],
        permission_classes=[IsAuthenticated],
    )
    def delete_avatar(self, request):
        """Удаление аватара пользователя."""
        if request.user.avatar:
            request.user.avatar.delete()
            request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeViewSet(viewsets.ModelViewSet):
    """Представление для управления рецептами."""

    queryset = Recipe.objects.all()
    filterset_class = RecipeFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        queryset = (
            Recipe.objects.all()
            .select_related('author')
            .prefetch_related('tags', 'ingredients')
        )

        if self.request.user.is_authenticated:
            user = self.request.user
            shopping_cart_exists = hasattr(user, 'shopping_cart')

            queryset = queryset.annotate(
                is_favorited=Exists(
                    user.favorite_recipes.filter(recipe=OuterRef('id'))
                )
                if hasattr(user, 'favorite_recipes') else Value(False),
                is_in_shopping_cart=Exists(
                    user.shopping_cart.recipe.filter(id=OuterRef('id'))
                )
                if shopping_cart_exists else Value(False),
            )
        else:
            queryset = queryset.annotate(
                is_in_shopping_cart=Value(False), is_favorited=Value(False)
            )
        return queryset

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_link']:
            permission_classes = [AllowAny]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthorOrAdminOrReadOnly]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeCreateUpdateSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['get'],
        url_path='get-link',
        permission_classes=[AllowAny],
    )
    def get_link(self, request, pk=None):
        """Получение прямой ссылки на рецепт."""
        try:
            recipe = self.get_object()
            direct_link = create_short_link(recipe.id, request)
            return Response(
                {'short-link': direct_link}, status=status.HTTP_200_OK
            )
        except Recipe.DoesNotExist:
            return Response(
                {'detail': 'Рецепт не найден'},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        """
        Представление для скачивания списка покупок в формате CSV.
        """
        shopping_cart = (
            request.user.shopping_cart.recipe.all().values(
                'ingredients__name', 'ingredients__measurement_unit'
            )
            .annotate(amount=Sum('recipe_ingredients__amount'))
            .order_by()
        )
        return generate_shopping_cart_csv(shopping_cart)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
        url_path='favorite',
    )
    def favorite(self, request, pk=None):
        """Добавление/удаление рецепта в избранное."""
        recipe = self.get_object()

        if request.method == 'POST':
            serializer = FavoriteRecipeSerializer(
                data={'recipe': recipe.id}, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)

            response_serializer = RecipeShortSerializer(
                recipe, context={'request': request}
            )
            return Response(
                response_serializer.data, status=status.HTTP_201_CREATED
            )

        favorite = request.user.favorite_recipes.filter(recipe=recipe)
        if not favorite.exists():
            return Response(
                {'errors': 'Рецепт не находится в избранном'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
        url_path='shopping_cart',
    )
    def shopping_cart(self, request, pk=None):
        """Добавление/удаление рецепта в список покупок."""
        recipe = self.get_object()

        if request.method == 'POST':
            serializer = ShoppingCartSerializer(
                data={'recipe': recipe.id}, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            response_serializer = RecipeShortSerializer(
                recipe, context={'request': request}
            )
            return Response(
                response_serializer.data, status=status.HTTP_201_CREATED
            )

        shopping_cart = request.user.shopping_cart
        if not shopping_cart.recipe.filter(id=recipe.id).exists():
            return Response(
                {'errors': 'Рецепт не находится в списке покупок'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        shopping_cart.recipe.remove(recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(RecipeAccessMixin, viewsets.ModelViewSet):
    """Список тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Управления ингредиентами."""

    queryset = Ingredient.objects.all().order_by('name')
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    permission_classes = [AllowAny]
    filterset_class = IngredientFilter
    search_fields = ('^name',)
    pagination_class = None
