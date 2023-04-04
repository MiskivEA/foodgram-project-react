from django.contrib import admin
from django.contrib.auth import get_user_model

from app.models import (Recipe, Tag, Ingredient, Cart,
                        FavoriteRecipes, IngredientRecipe, Amount, MeasurementUnit)

from users.models import Follow

User = get_user_model()

admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(IngredientRecipe)
admin.site.register(Cart)
admin.site.register(Follow)
admin.site.register(FavoriteRecipes)
admin.site.register(User)
admin.site.register(Amount)
admin.site.register(MeasurementUnit)
