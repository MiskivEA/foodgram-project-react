from django.core.validators import RegexValidator
from django.db import models

from foodgram import settings

User = settings.AUTH_USER_MODEL


class Recipe(models.Model):
    """Рецепт"""
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipe')

    name = models.CharField(max_length=200,
                            verbose_name='Название')

    image = models.BinaryField(max_length=None)
    text = models.TextField(max_length=None)
    ingredients = models.ManyToManyField('Ingredient',
                                         related_name='ingredients')


class Tag(models.Model):
    """Тэг"""
    name = models.CharField(max_length=200,
                            unique=True)
    color = models.CharField(max_length=7,
                             unique=True, )
    slug = models.SlugField(max_length=200,
                            unique=True,
                            validators=[RegexValidator(
                                regex='^[-a-zA-Z0-9_]+$')]
                            )


class Ingredient(models.Model):
    """Ингридиент"""
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)


class Cart(models.Model):
    """Корзина"""
    name = models.CharField(max_length=200)
    recipes = models.ForeignKey(Recipe,
                                on_delete=models.CASCADE,
                                related_name='carts')
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='users')


class Follow(models.Model):
    """Подписки пользователей друг на друга"""
    user = models.ForeignKey(
        User,
        related_name='followers',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name='followings',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.user} > подписан на > {self.author}'


class FavoriteRecipes(models.Model):
    """Избранные рецепты пользоваьелей"""
    user = models.ForeignKey(User,
                             related_name='favorite_recipes',
                             on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE)
