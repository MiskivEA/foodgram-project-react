from django.urls import include, path
from users.urls import router_v1

from .views import IngredientViewSet, RecipeViewSet, TagViewSet

app_name = 'api'


router_v1.register(r'recipes', RecipeViewSet)
router_v1.register(r'tags', TagViewSet)
router_v1.register(r'ingredients', IngredientViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
]
