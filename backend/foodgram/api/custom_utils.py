from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters

from app.models import Cart

User = get_user_model()


class CustomPaginationClass(PageNumberPagination):
    page_size = 6


class FavoriteFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        is_favorited = request.query_params.get('is_favorited')
        is_in_shopping_cart = request.query_params.get('is_in_shopping_cart')
        tags = request.query_params.getlist('tags')

        if is_in_shopping_cart is not None:
            new_q_carts = request.user.carts.all()
            queryset = [item.recipe for item in new_q_carts]

        if is_favorited is not None:
            new_q_favorite = request.user.favorite_recipes.all()
            queryset = [item.recipe for item in new_q_favorite]

        if tags is not None:
            if len(tags) > 0:
                queryset = queryset.filter(tag__slug__in=tags)
        print(queryset)
        return queryset