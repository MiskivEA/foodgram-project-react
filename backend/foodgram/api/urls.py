from django.urls import path, include


from .views import (RecipeViewSet, TagViewSet, IngredientViewSet)

from users.urls import router_v1


app_name = 'api'


router_v1.register(r'recipes', RecipeViewSet)
router_v1.register(r'tags', TagViewSet)
router_v1.register(r'ingredients', IngredientViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
]
