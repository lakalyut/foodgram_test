import os

from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from .test_recipes_data import TEST_RECIPES

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates test recipes'

    def handle(self, *args, **options):
        required_tags = ['breakfast', 'lunch', 'dinner']
        existing_tags = Tag.objects.filter(slug__in=required_tags)
        if len(existing_tags) != len(required_tags):
            self.stdout.write(
                self.style.ERROR('Необходимые теги не существуют')
            )
            return

        for i in range(1, 11):
            username = f'testuser{i}'
            if not User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.ERROR(f'Пользователь {username} отсутствует')
                )
                return

        image_folder = 'recipes/management/commands/test_pics/'

        if not os.path.exists(image_folder):
            self.stdout.write(
                self.style.ERROR(f'Папк {image_folder} отсутствует')
            )
            return

        recipes_created = 0

        for user_index in range(10):
            username = f'testuser{user_index + 1}'
            user = User.objects.get(username=username)

            for recipe_index in range(3):
                recipe_data_index = user_index * 3 + recipe_index
                if recipe_data_index >= len(TEST_RECIPES):
                    break

                recipe_data = TEST_RECIPES[recipe_data_index]

                try:
                    ingredients_exist = all(
                        Ingredient.objects.filter(name=ing_name).exists()
                        for ing_name, _ in recipe_data['ingredients']
                    )

                    if not ingredients_exist:
                        self.stdout.write(
                            self.style.WARNING(
                                f'{recipe_data["name"]} не найден'
                            )
                        )
                        continue

                    image_index = recipe_data_index + 1
                    image_path = os.path.join(
                        image_folder, f'test_pic{image_index}.jpg'
                    )
                    if not os.path.exists(image_path):
                        self.stdout.write(
                            self.style.WARNING(f'{image_index}.jpg не найден')
                        )
                        continue

                    recipe = Recipe.objects.create(
                        author=user,
                        name=recipe_data['name'],
                        text=recipe_data['text'],
                        cooking_time=recipe_data['cooking_time'],
                    )

                    with open(image_path, 'rb') as img_file:
                        recipe.image.save(
                            f'test_pic{image_index}.jpg',
                            File(img_file),
                            save=True,
                        )

                    for tag_slug in recipe_data['tags']:
                        tag = Tag.objects.get(slug=tag_slug)
                        recipe.tags.add(tag)

                    for ing_name, amount in recipe_data['ingredients']:
                        try:
                            ingredient = Ingredient.objects.get(name=ing_name)
                            RecipeIngredient.objects.create(
                                recipe=recipe,
                                ingredient=ingredient,
                                amount=amount,
                            )
                        except Ingredient.DoesNotExist:
                            self.stdout.write(
                                self.style.WARNING('Ингридиента нет в базе')
                            )
                            continue

                    recipes_created += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Создан рецепт: {recipe_data["name"]}'
                        )
                    )

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Ошибка создания {recipe_data["name"]}: {str(e)}'
                        )
                    )

        self.stdout.write(
            self.style.SUCCESS(f'Успешно создано {recipes_created}')
        )
