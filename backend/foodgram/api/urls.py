from django.urls import path, include


from .views import (RecipeViewSet, TagViewSet, IngredientViewSet)

from users.urls import router_v1


app_name = 'api'


router_v1.register(r'api/recipes', RecipeViewSet)
router_v1.register(r'api/tags', TagViewSet)
router_v1.register(r'api/ingredients', IngredientViewSet)
router_v1.register('', RecipeViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
]
