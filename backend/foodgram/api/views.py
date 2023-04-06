from django.http import JsonResponse, FileResponse
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from djoser.views import UserViewSet as BaseUserViewSet

from api.serializers import (RecipeSerializer,
                             TagSerializer,
                             FavoriteRecipesSerializer,
                             RecipeSerializerForCart, RecipeSerializerWrite, IngredientSerializer,
                             IngredientAmountSerializer, )
                             #IngredientRecipeSerializerWrite

from app.models import *
from users.models import Follow
from users.serializers import FollowSerializer


class CustomPaginationClass(PageNumberPagination):
    page_size = 5


# class IngredientRecipeViewSet(viewsets.ModelViewSet):
#     queryset = IngredientAmount.objects.all()
#     permission_classes = permissions.AllowAny,
#     pagination_class = CustomPaginationClass
#     serializer_class = IngredientAmountSerializer

    # def get_serializer_class(self):
    #     if self.request.method == 'GET':
    #         return IngredientRecipeSerializer
    #     elif self.request.method in ['POST', 'PUT', 'PATCH']:
    #         return IngredientRecipeSerializerWrite
    #     else:
    #         return RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = permissions.AllowAny,
    pagination_class = CustomPaginationClass

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        elif self.request.method in ['POST', 'PUT', 'PATCH']:
            return RecipeSerializerWrite
        else:
            return RecipeSerializer


    @action(methods=['post', 'delete'],
            detail=True)
    def shopping_cart(self, request, pk):
        user = request.user
        recipe = Recipe.objects.get(pk=pk)

        if request.method == 'POST':
            _, created = Cart.objects.get_or_create(recipe=recipe, owner=user)
            if not created:
                return Response({'errors': 'Ошибка добавления в список покупок(уже добавлено)'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = RecipeSerializerForCart(recipe, many=False)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            try:
                Cart.objects.get(recipe=recipe, owner=user).delete()
                return Response(status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'errors': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'],
            detail=False)
    def download_shopping_cart(self, request):
        user = request.user
        user_cart_queryset = user.carts.all()
        print(list(user_cart_queryset.values()))
        return Response(status=status.HTTP_200_OK)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class FavoriteRecipesViewSet(viewsets.ModelViewSet):
    queryset = FavoriteRecipes.objects.all()
    serializer_class = FavoriteRecipesSerializer


class UserViewSet(BaseUserViewSet):
    pagination_class = CustomPaginationClass
