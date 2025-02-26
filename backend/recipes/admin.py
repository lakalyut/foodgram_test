from django.contrib import admin

from .models import (
    FavoriteRecipe,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Subscribe,
    Tag
)


class RecipeIngredientAdmin(admin.StackedInline):
    """Управление ингредиентами в рецепте."""

    model = RecipeIngredient
    autocomplete_fields = ('ingredient',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Управление рецептами."""

    list_display = (
        'id',
        'get_author',
        'name',
        'cooking_time',
        'get_tags',
        'get_ingredients',
        'pub_date',
        'get_favorite_count'
    )
    search_fields = (
        'name',
        'cooking_time',
        "author__email",
        'ingredients__name'
    )
    list_filter = (
        'pub_date',
        'tags'
    )
    inlines = (RecipeIngredientAdmin,)
    empty_value_display = '  '

    @admin.display(description='e-mail автора')
    def get_author(self, obj):
        """Возвращает e-mail автора рецепта."""
        return obj.author.email

    @admin.display(description='Теги')
    def get_tags(self, obj):
        """Возвращает список тегов."""
        return ', '.join(tag.name for tag in obj.tags.all())

    @admin.display(description='Ингредиенты')
    def get_ingredients(self, obj):
        """Возвращает список ингредиентов."""
        return '\n '.join(
            f'{item["ingredient__name"]} - {item["amount"]} '
            f'{item["ingredient__measurement_unit"]}.'
            for item in obj.recipe.values(
                'ingredient__name',
                'amount',
                'ingredient__measurement_unit'
            )
        )

    @admin.display(description='В избранном')
    def get_favorite_count(self, obj):
        """Возвращает добавления рецепта в избранное."""
        return obj.favorited_by.count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Управление тегами."""

    list_display = (
        'id',
        'name',
        'slug'
    )
    search_fields = (
        'name',
        'slug'
    )
    empty_value_display = '  '


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Управление ингредиентами."""

    list_display = (
        'id',
        'name',
        'measurement_unit'
    )
    search_fields = (
        'name',
        'measurement_unit'
    )
    empty_value_display = '  '


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    """Управление подписками."""

    list_display = (
        'id',
        'user',
        'author',
        'created',
    )
    search_fields = (
        'user__email',
        'author__email'
    )
    empty_value_display = '  '


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    """Управление израбнными рецептами."""

    list_display = (
        'id',
        'user',
        'get_recipe',
        'get_count',
    )
    empty_value_display = '  '

    @admin.display(description='Рецепты')
    def get_recipe(self, obj):
        """Возвращает первые пять рецептов в избранном."""

        return [f'{item["name"]} ' for item in obj.recipe.values('name')[:5]]

    @admin.display(description='В избранном')
    def get_count(self, obj):
        """Количество рецептов в избранном."""

        return obj.recipe.count()


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Управление корзиной покупок."""

    list_display = (
        'id',
        'user',
        'get_recipe',
        'get_count',
    )
    empty_value_display = '  '

    @admin.display(description='Рецепты')
    def get_recipe(self, obj):
        """Возвращает первые пять рецептов в корзине."""

        return [f'{item["name"]} ' for item in obj.recipe.values('name')[:5]]

    @admin.display(description='В избранном')
    def get_count(self, obj):
        """Количество рецептов в избранном."""

        return obj.recipe.count()
