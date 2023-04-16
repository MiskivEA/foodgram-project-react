import rest_framework.pagination
from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework import filters
import urllib.parse

User = get_user_model()


class CustomPaginationClass(LimitOffsetPagination):
    """Оставлю возможность настройки здесь =)"""
    pass


class RecipeFilter(filters.BaseFilterBackend):
    """Кастомный фильтр рецептов по тегам, избранным,
    и по наличию рецепта в корзине у текущего пользователя"""

    def filter_queryset(self, request, queryset, view):
        is_favorited = request.query_params.get('is_favorited')
        is_in_shopping_cart = request.query_params.get('is_in_shopping_cart')
        tags = request.query_params.getlist('tags')

        if is_in_shopping_cart is not None:
            user_cart = request.user.carts.all()
            user_cart_recipes_ids = [item.recipe.id for item in user_cart]
            queryset = queryset.filter(id__in=user_cart_recipes_ids)

        if is_favorited is not None:
            favorites = request.user.favorite_recipes.all()
            favorite_recipes_ids = [item.recipe.id for item in favorites]
            queryset = queryset.filter(id__in=favorite_recipes_ids)

        if tags is not None:
            if len(tags) > 0:
                queryset = queryset.filter(tag__slug__in=tags)

        return queryset.distinct()


class RussianSearchFilter(filters.BaseFilterBackend):
    """Стандарный SearchFilter не принимает кирилицу для поиска,
    а точнее закодированную кирилицу из запроса,
    для этого здесь этот кастомный фильтр."""

    def filter_queryset(self, request, queryset, view):
        param = request.query_params.get('name')
        decoded_param = urllib.parse.unquote(param)
        queryset = queryset.filter(name__startswith=decoded_param)
        return queryset
