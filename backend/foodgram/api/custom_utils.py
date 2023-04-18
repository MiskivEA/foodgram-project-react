from django.contrib.auth import get_user_model
from rest_framework.pagination import  LimitOffsetPagination
from rest_framework import filters, permissions
import urllib.parse

User = get_user_model()


class CustomPaginationClass(LimitOffsetPagination):
    """Оставлю возможность настройки здесь """
    pass


class RecipeFilter(filters.BaseFilterBackend):
    """Кастомный фильтр рецептов по тегам, избранным,
    и по наличию рецепта в корзине у текущего пользователя.
    И еще по авторам"""

    def filter_queryset(self, request, queryset, view):
        is_favorited = request.query_params.get('is_favorited')
        is_in_shopping_cart = request.query_params.get('is_in_shopping_cart')
        tags = request.query_params.getlist('tags')
        author_id = request.query_params.get('author')

        if is_in_shopping_cart is not None:
            user_cart = request.user.carts.all()
            user_cart_recipes_ids = [item.recipe.id for item in user_cart]
            queryset = queryset.filter(id__in=user_cart_recipes_ids)

        if is_favorited is not None:
            favorites = request.user.favorite_recipes.all()
            favorite_recipes_ids = [item.recipe.id for item in favorites]
            queryset = queryset.filter(id__in=favorite_recipes_ids)

        if author_id is not None:
            queryset = queryset.filter(author__id=author_id)

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


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user == obj.author
        )