from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models

User = get_user_model()


class Recipe(models.Model):
    """Рецепт"""
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор рецепта')

    name = models.CharField(max_length=200,
                            verbose_name='Название')

    image = models.ImageField(upload_to='images/', blank=True)
    text = models.TextField(max_length=None)
    ingredients = models.ManyToManyField('IngredientAmount',
                                         related_name='recipes',
                                         blank=True,
                                         verbose_name='Ингридиенты')
    tag = models.ManyToManyField('Tag',
                                 related_name='recipes',
                                 blank=True)
    cooking_time = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)
    how_mach_time_add_to_favorite = models.IntegerField(default=0)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.name}'


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

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.slug


class Ingredient(models.Model):
    """Модель ингридинета
    Включает название и в чем измеряется его количество"""

    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class IngredientAmount(models.Model):
    """Ингридиент
    Название и количество в рецепте"""
    name = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='ingredients')
    amount = models.IntegerField()

    class Meta:
        verbose_name = 'Ингридиент - количество'
        verbose_name_plural = 'Ингридиент - количество'

    def __str__(self):
        return f' {self.name}:  {self.amount}'


class Cart(models.Model):
    """Корзина"""
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='carts')
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='carts')

    class Meta:
        unique_together = ('recipe', 'owner')
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'{self.owner}:{self.recipe}'


class FavoriteRecipes(models.Model):
    """Избранные рецепты пользоваьелей"""
    user = models.ForeignKey(User,
                             related_name='favorite_recipes',
                             on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return f'Пользователь: {self.user} Избранный рецепт: {self.recipe}'
