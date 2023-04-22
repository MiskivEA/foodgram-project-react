import urllib.parse

from django.contrib.auth import get_user_model
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination as Lop

User = get_user_model()


class LimitOffsetPagination(Lop):
    """Оставлю возможность настройки здесь """
    pass


class RecipeFilter(filters.BaseFilterBackend):
    """Кастомный фильтр рецептов по тегам, избранным,
    и по наличию рецепта в корзине у текущего пользователя.
    И еще по авторам"""

    def filter_queryset(self, request, queryset, view):
        anon = request.user.is_anonymous

        is_favorited = request.query_params.get('is_favorited')
        is_in_shopping_cart = request.query_params.get('is_in_shopping_cart')
        tags = request.query_params.getlist('tags')
        author_id = request.query_params.get('author')

        if is_in_shopping_cart is not None:
            if anon:
                return None
            user_cart = request.user.carts.select_related('recipe').all()
            favorite_recipes_ids = [item.recipe.id for item in user_cart]
            queryset = queryset.filter(id__in=favorite_recipes_ids)

        if is_favorited is not None:
            if anon:
                return None
            favorites = request.user.favorite_recipes.select_related('recipe').all()
            favorite_recipes_ids = [item.recipe.id for item in favorites]
            queryset = queryset.filter(id__in=favorite_recipes_ids)

        if author_id is not None:
            if anon:
                return None
            queryset = queryset.filter(author__id=author_id)

        if tags is not None:
            if len(tags) > 0:
                queryset = queryset.filter(tags__slug__in=tags).distinct()

        return queryset


class RussianSearchFilter(filters.BaseFilterBackend):
    """Стандарный SearchFilter не принимает кирилицу для поиска,
    а точнее закодированную кирилицу из запроса,
    для этого здесь этот кастомный фильтр."""

    def filter_queryset(self, request, queryset, view):
        param = request.query_params.get('name')
        if param is not None:
            decoded_param = urllib.parse.unquote(param)
            return queryset.filter(name__startswith=decoded_param)
        return queryset
