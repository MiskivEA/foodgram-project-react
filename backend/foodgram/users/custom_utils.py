from django.contrib.auth import get_user_model
from rest_framework import filters

User = get_user_model()


class RecipeFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        is_subscribed = request.query_params.get('is_subscribed')

        if is_subscribed is not None:
            queryset = queryset.filter()

        print(queryset)
        return queryset
