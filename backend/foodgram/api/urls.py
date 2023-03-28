from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (RecipeViewSet, TagViewSet, IngredientViewSet,
                   CartViewSet, FollowViewSet, FavoriteRecipesViewSet, UserViewSet)


app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(r'recipes', RecipeViewSet)
router_v1.register(r'tags', TagViewSet)
router_v1.register(r'ingredient', IngredientViewSet)
router_v1.register(r'recipes/(?P<recipe_id>\d+)/shopping_cart', CartViewSet)
router_v1.register(r'users/subscriptions', FollowViewSet)
router_v1.register(r'recipes/(?P<recipe_id>\d+)/favorite', FavoriteRecipesViewSet)
router_v1.register(r'users', UserViewSet)


urlpatterns = [
    path('v1/', include(router_v1.urls)),

]
