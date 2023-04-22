from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.custom_utils import (LimitOffsetPagination, RecipeFilter,
                              RussianSearchFilter)
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (IngredientSerializer,
                             RecipeCreateUpdateSerializer,
                             RecipeListSerializer, RecipeSerializerForCart,
                             TagSerializer)
from app.models import (Cart, FavoriteRecipes, Ingredient, Recipe,
                        RecipeIngredient, Tag)

User = get_user_model()


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly)
    pagination_class = LimitOffsetPagination
    filter_backends = RecipeFilter,

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RecipeCreateUpdateSerializer
        return RecipeListSerializer

    @action(methods=['post', 'delete'],
            detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def shopping_cart(self, request, pk):
        """Добавление рецепта в корзину"""
        user = request.user
        recipe = Recipe.objects.get(pk=pk)

        if request.method == 'POST':
            _, created = Cart.objects.get_or_create(recipe=recipe, owner=user)
            if not created:
                return Response({
                    'errors': 'Ошибка добавления в список покупок'},
                    status=status.HTTP_400_BAD_REQUEST)
            serializer = RecipeSerializerForCart(recipe, many=False)
            return JsonResponse(serializer.data,
                                status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            get_object_or_404(Cart, recipe=recipe, owner=user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'],
            detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        """Формирование списка покупок на основании
        рецептов в корзине и его скачивание"""

        user = request.user
        ingredient_amount_list = RecipeIngredient.objects.filter(
            recipe__carts__owner=user).values('ingredient__name', 'ingredient__measurement_unit'
                                              ).annotate(total=Sum('amount'))

        text = ''
        for i in ingredient_amount_list:
            text += (
                f'{i["ingredient__name"]} - '
                f'{i["total"]} '
                f'({i["ingredient__measurement_unit"]}) \n'
            )

        file_name = 'shopping_cart.txt'
        file_location = f'files/{file_name}'
        with open(file_location, 'w') as file:
            file.write(text)

        with open(file_location, 'r') as f:
            file_data = f.read()
            response = FileResponse(file_data, content_type='text')
            response[
                'Content-Disposition'] = f'attachment; filename={file_name}'

        return response

    @action(methods=['post', 'delete'],
            detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk):
        """Добавление рецепта в избранные рецепты"""
        user = request.user
        recipe = Recipe.objects.get(pk=pk)
        if request.method == 'POST':
            favorite, is_created = FavoriteRecipes.objects.get_or_create(
                user=user, recipe=recipe)
            if is_created:
                serializer = RecipeSerializerForCart(recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(
                {'error': 'The Recipe is already in your favorites list'})
        if request.method == 'DELETE':
            get_object_or_404(FavoriteRecipes, user=user, recipe=recipe).delete()
            return Response(status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = RussianSearchFilter,
