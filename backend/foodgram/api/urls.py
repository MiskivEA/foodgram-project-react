from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (RecipeViewSet, TagViewSet, IngredientViewSet,
                   CartViewSet, FollowViewSet, FavoriteRecipesViewSet)


app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(r'recipes', RecipeViewSet)
router_v1.register(r'tags', TagViewSet)
router_v1.register(r'ingredients', IngredientViewSet)
router_v1.register(r'recipes/(?P<recipe_id>\d+)/shopping_cart', CartViewSet)
router_v1.register(r'users/subscriptions', FollowViewSet)
router_v1.register(r'recipes/(?P<recipe_id>\d+)/favorite', FavoriteRecipesViewSet)


urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))


]
