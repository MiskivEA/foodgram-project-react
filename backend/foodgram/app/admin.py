from django.contrib import admin

from .models import Recipe, Tag, Ingredient, Cart, Follow, FavoriteRecipes

admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Cart)
admin.site.register(Follow)
admin.site.register(FavoriteRecipes)

