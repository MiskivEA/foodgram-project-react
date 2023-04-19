from api.custom_utils import (CustomPaginationClass, IsAuthorOrReadOnly,
                              RecipeFilter, RussianSearchFilter)
from api.serializers import (FavoriteRecipesSerializer, IngredientSerializer,
                             RecipeSerializer, RecipeSerializerForCart,
                             RecipeSerializerWrite, TagSerializer)
from app.models import Cart, FavoriteRecipes, Ingredient, Recipe, Tag
from django.contrib.auth import get_user_model
from django.http import FileResponse, JsonResponse
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import Follow
from users.serializers import FollowSerializer

User = get_user_model()


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly)
    pagination_class = CustomPaginationClass
    filter_backends = RecipeFilter,

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RecipeSerializerWrite
        return RecipeSerializer

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
        elif request.method == 'DELETE':
            try:
                Cart.objects.get(recipe=recipe, owner=user).delete()
                return Response(status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'errors': f'{e}'},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(methods=['get'],
            detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        """Формирование списка покупок на основании
        рецептов в корзине и его скачивание"""

        user = request.user
        user_cart_queryset = user.carts.all()
        recipes_list = [cart.recipe for cart in user_cart_queryset]
        ingredient_amount_list = []
        counter = {}
        for recipe in recipes_list:
            ingredient_amount_list.append(recipe.ingredients.all())
        for ingredient_amount in ingredient_amount_list:
            for ingredient in ingredient_amount:
                if ingredient.name in counter:
                    counter[ingredient.name] += ingredient.amount
                else:
                    counter[ingredient.name] = ingredient.amount
        file_name = 'shopping_cart.txt'
        file_location = f'files/{file_name}'
        with open(file_location, 'w') as file:
            for ingredient, amount in counter.items():
                file.write(
                    f'{ingredient.name} '
                    f'[{ingredient.measurement_unit}] --- {amount} \n')

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
                count = FavoriteRecipes.objects.filter(recipe=recipe).count()
                recipe.how_mach_time_add_to_favorite = count
                recipe.save()

                serializer = RecipeSerializerForCart(recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(
                {'error': 'The Recipe is already in your favorites list'})
        elif request.method == 'DELETE':
            try:
                FavoriteRecipes.objects.get(user=user, recipe=recipe).delete()
                count = FavoriteRecipes.objects.filter(recipe=recipe).count()
                recipe.how_mach_time_add_to_favorite = count
                recipe.save()
                return Response(status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response({'error': f'{e}'},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = RussianSearchFilter,


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class FavoriteRecipesViewSet(viewsets.ModelViewSet):
    queryset = FavoriteRecipes.objects.all()
    serializer_class = FavoriteRecipesSerializer
