from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import (Recipe, Tag, Ingredient, Cart, Follow,
                     FavoriteRecipes, IngredientsAmount)

User = get_user_model()

admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Cart)
admin.site.register(Follow)
admin.site.register(FavoriteRecipes)
admin.site.register(IngredientsAmount)
admin.site.register(User)
