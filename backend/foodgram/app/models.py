from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models

User = get_user_model()


class Recipe(models.Model):
    """Рецепт"""
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes')

    name = models.CharField(max_length=200,
                            verbose_name='Название')

    image = models.BinaryField(max_length=None)
    text = models.TextField(max_length=None)
    ingredients = models.ManyToManyField('IngredientRecipe',
                                         related_name='recipes')
    tag = models.ManyToManyField('Tag',
                                 related_name='recipes')
    cooking_time = models.IntegerField()

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

    def __str__(self):
        return self.slug


class MeasurementUnit(models.Model):
    measurement_unit = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.measurement_unit}'


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.ForeignKey(MeasurementUnit, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class Amount(models.Model):
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.amount}'


class IngredientRecipe(models.Model):
    """Ингридиент
    Название и единица меры"""
    name = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField()
    measurement_unit = models.ForeignKey(MeasurementUnit, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}:  {self.amount} {self.measurement_unit}'


class Cart(models.Model):
    """Корзина"""
    name = models.CharField(max_length=200,
                            blank=True)
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='carts')
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='carts')

    class Meta():
        unique_together = ('recipe', 'owner')

    def __str__(self):
        return f'{self.owner}:{self.name}'


class FavoriteRecipes(models.Model):
    """Избранные рецепты пользоваьелей"""
    user = models.ForeignKey(User,
                             related_name='favorite_recipes',
                             on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE)

    def __str__(self):
        return f'Пользователь: {self.user} Избранный рецепт: {self.recipe}'
