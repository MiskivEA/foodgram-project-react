from django.http import JsonResponse
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from djoser.views import UserViewSet as BaseUserViewSet

from api.serializers import (RecipeSerializer, CartSerializer,
                             TagSerializer, IngredientsAmountSerializer,
                             FollowSerializer, FavoriteRecipesSerializer,
                             RecipeSerializerForCart)
from app.models import *


class CustomPaginationClass(PageNumberPagination):
    page_size = 5


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = permissions.AllowAny,
    pagination_class = CustomPaginationClass

    @action(methods=['post', 'delete'],
            detail=True)
    def shopping_cart(self, request, pk):
        user = request.user
        recipe = Recipe.objects.get(pk=pk)

        if request.method == 'POST':
            Cart.objects.get_or_create(recipe=recipe, owner=user)
            serializer = RecipeSerializerForCart(recipe, many=False)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            try:
                Cart.objects.get(recipe=recipe, owner=user).delete()
                return Response(status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'errors': f'{e}'})


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsAmountSerializer


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class FavoriteRecipesViewSet(viewsets.ModelViewSet):
    queryset = FavoriteRecipes.objects.all()
    serializer_class = FavoriteRecipesSerializer


class UserViewSet(BaseUserViewSet):
    pagination_class = CustomPaginationClass
