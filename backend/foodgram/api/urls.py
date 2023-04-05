from django.urls import path, include

from .views import (RecipeViewSet, TagViewSet,
                    FollowViewSet, FavoriteRecipesViewSet, IngredientViewSet, IngredientRecipeViewSet)

from users.urls import router_v1


app_name = 'api'


router_v1.register(r'recipes', RecipeViewSet)
router_v1.register(r'tags', TagViewSet)
router_v1.register(r'ingredients', IngredientViewSet)
router_v1.register(r'ingredients-recipe', IngredientRecipeViewSet)

# router_v1.register(r'recipes/(?P<recipe_id>\d+)/shopping_cart', CartViewSet)
router_v1.register(r'users/subscriptions', FollowViewSet)
# router_v1.register(r'recipes/(?P<recipe_id>\d+)/favorite', FavoriteRecipesViewSet)


urlpatterns = [
    path('', include(router_v1.urls)),
]
