from django.http import JsonResponse, FileResponse, HttpResponse, HttpResponseNotFound
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from djoser.views import UserViewSet as BaseUserViewSet

from api.serializers import (RecipeSerializer,
                             TagSerializer,
                             FavoriteRecipesSerializer,
                             RecipeSerializerForCart, RecipeSerializerWrite, IngredientSerializer,
                             CartSerializer, )

from app.models import Recipe, Cart, FavoriteRecipes, Tag, Ingredient
from users.models import Follow
from users.serializers import FollowSerializer


class CustomPaginationClass(PageNumberPagination):
    page_size = 5


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
                return Response({'errors': 'Ошибка добавления в список покупок(уже добавлено)'},
                                status=status.HTTP_400_BAD_REQUEST)
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
        """Скачивание списка рецептов из корзины текущего пользователя"""
        user = request.user
        user_cart_queryset = user.carts.all()

        file_location = 'files/shopping_cart.txt'
        with open(file_location, 'w') as file:
            for obj in user_cart_queryset:
                file.write(obj.recipe.name + '\n')

        with open(file_location, 'r') as f:
            file_data = f.read()
            response = FileResponse(file_data)
            response['Content-Disposition'] = 'attachment; filename="my_shopping_cart.txt"'

        return response

    @action(methods=['post', 'delete'],
            detail=True)
    def favorite(self, request, pk):
        user = request.user
        recipe = Recipe.objects.get(pk=pk)
        if request.method == 'POST':
            favorite, is_created = FavoriteRecipes.objects.get_or_create(
                user=user, recipe=recipe)
            if is_created:
                serializer = RecipeSerializerForCart(recipe)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'error': 'The Recipe is already in your favorites list'})
        elif request.method == 'DELETE':
            try:
                FavoriteRecipes.objects.get(user=user, recipe=recipe).delete()
                return Response(status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



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
