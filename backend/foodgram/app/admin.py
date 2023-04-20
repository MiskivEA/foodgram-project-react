from django.contrib import admin
from django.contrib.auth import get_user_model
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin

from app.models import (Cart, FavoriteRecipes, Ingredient, Recipe,
                        RecipeIngredient, Tag)
from users.models import Follow

User = get_user_model()


class IngredientInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 2


class UserAdmin(admin.ModelAdmin):
    list_filter = 'email', 'username'


class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'author', 'favorite_count']
    list_filter = 'name', 'author'
    search_fields = 'name',
    inlines = [IngredientInLine]

    def favorite_count(self, obj):
        if FavoriteRecipes.objects.filter(recipe=obj).exists():
            return FavoriteRecipes.objects.filter(recipe=obj).count()
        return 0


class IngredientResource(resources.ModelResource):
    class Meta:
        model = Ingredient
        fields = 'id', 'name', 'measurement_unit'


class IngredientAdmin(ImportExportActionModelAdmin):
    resource_class = IngredientResource


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredient)
admin.site.register(Cart)
admin.site.register(User, UserAdmin)
admin.site.register(Follow)
admin.site.register(FavoriteRecipes)
