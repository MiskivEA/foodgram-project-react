from django.http import JsonResponse, FileResponse
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from djoser.views import UserViewSet as BaseUserViewSet


from app.models import *
from users.models import Follow
from users.serializers import FollowSerializer


class CustomPaginationClass(PageNumberPagination):
    page_size = 5


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class UserViewSet(BaseUserViewSet):
    pagination_class = CustomPaginationClass
