from django.contrib.auth import get_user_model
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from api import constants

User = get_user_model()


class Tag(models.Model):
    """Модель для тегов."""

    name = models.CharField(
        'Название', max_length=constants.TAG_NAME_FIELD_LENGTH, unique=True
    )
    slug = models.SlugField(
        'Ссылка',
        max_length=constants.TAG_SLUG_FIELD_LENGTH,
        unique=True,
        null=True,
        validators=[RegexValidator(regex='^[-a-zA-Z0-9_]+$')]
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель для ингредиентов."""

    name = models.CharField(
        'Название ингредиента',
        max_length=constants.INGREDIENT_NAME_FIELD_LENGTH
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=constants.MEASUREMENT_UNIT_FIELD_LENGTH
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    """Модель для рецептов."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        'Название рецепта', max_length=constants.RECIPE_NAME_FIELD_LENGTH
    )
    image = models.ImageField(
        'Изображение рецепта',
        upload_to='static/recipe/',
        null=True
    )
    text = models.TextField('Описание рецепта')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[
            MinValueValidator(
                constants.MIN_MEANING,
                message=constants.COOKING_TIME_MESSAGE_ERROR
            ),
            MaxValueValidator(
                constants.MAX_MEANING,
                message=constants.COOKING_TIME_MESSAGE_ERROR
            )

        ]
    )
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient'
    )
    tags = models.ManyToManyField(
        Tag, verbose_name='Теги', related_name='recipes'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return f'{self.author.email}, {self.name}'


class RecipeIngredient(models.Model):
    """Модель для связи ингредиентов с рецептами."""

    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='recipe_ingredients'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        default=constants.MIN_MEANING,
        validators=[
            MinValueValidator(
                constants.MIN_MEANING,
                message=constants.AMOUNT_MESSAGE_ERROR
            ),
            MaxValueValidator(
                constants.MAX_MEANING,
                message=constants.AMOUNT_MESSAGE_ERROR
            ),
        ]
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'], name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.recipe.name} - {self.ingredient.name}: {self.amount}'


class Subscribe(models.Model):
    """Модель для подписок"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )
    created = models.DateTimeField('Дата подписки', auto_now_add=True)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_subscription'
            )
        ]

    def __str__(self):
        return f'Пользователь {self.user} - автор {self.author}'


class FavoriteRecipe(models.Model):
    """Модель для избраннного"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='fvorite_recipes',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name='Избранный рецепт'
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_favorite_recipe'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил {self.recipe.name} в избранное'


class ShoppingCart(models.Model):
    """Модель для корзины"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        null=True,
        verbose_name='Пользователь'
    )
    recipe = models.ManyToManyField(
        Recipe,
        related_name='shopping_cart',
        verbose_name='Покупка'
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        ordering = ['-id']

    def __str__(self):
        list_ = [item['name'] for item in self.recipe.values('name')]
        return f'Пользователь {self.user} добавил {list_} в покупки.'

    @staticmethod
    @receiver(post_save, sender=User)
    def create_shopping_cart(sender, instance, created, **kwargs):
        """Создание объекта корзины при создании пользователя"""
        if created:
            return ShoppingCart.objects.create(user=instance)
