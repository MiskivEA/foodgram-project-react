from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters

User = get_user_model()


class CustomPaginationClass(PageNumberPagination):
    page_size = 6


class FavoriteFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        # request.user = User.objects.get(pk=1) it`s for test
        is_favorited = request.query_params.get('is_favorited')
        print(is_favorited)
        if is_favorited is not None:
            new_q = request.user.favorite_recipes.all()
            queryset = [item.recipe for item in new_q]
        return queryset
