from app.models import (Cart, FavoriteRecipes, Ingredient, IngredientAmount,
                        Recipe, Tag)
from django.contrib import admin
from django.contrib.auth import get_user_model
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from users.models import Follow

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_filter = 'email', 'username'


class RecipeAdmin(admin.ModelAdmin):
    list_filter = 'name', 'author', 'tag'


class IngredientResource(resources.ModelResource):

    class Meta():
        model = Ingredient
        fields = 'id', 'name', 'measurement_unit'


class IngredientAdmin(ImportExportActionModelAdmin):
    resource_class = IngredientResource


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientAmount)
admin.site.register(Cart)
admin.site.register(User, UserAdmin)
admin.site.register(Follow)
admin.site.register(FavoriteRecipes)
