from django.contrib.auth import get_user_model

from rest_framework import serializers

from app.models import Recipe, Tag, Ingredient, Cart, FavoriteRecipes, IngredientRecipe
from users.serializers import UserSerializer

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientRecipeSerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(queryset=Ingredient.objects.all(),
                                        slug_field='name')
    measurement_unit = serializers.SlugRelatedField(queryset=Ingredient.objects.all(),
                                                    slug_field='measurement_unit')

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientRecipeSerializerWriteRecipe(serializers.ModelSerializer):
    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientRecipeSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, source='tag', read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = UserSerializer()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def is_no_authenticated(self):
        return self.context['request'].user.is_anonymous

    def get_user(self):
        return self.context['request'].user

    def get_is_favorited(self, obj):
        if self.is_no_authenticated():
            return False
        return FavoriteRecipes.objects.filter(user=self.get_user(), recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        if self.is_no_authenticated():
            return False
        return Cart.objects.filter(owner=self.get_user(), recipe=obj).exists()


class RecipeSerializerWrite(serializers.ModelSerializer):
    ingredients = IngredientRecipeSerializerWriteRecipe(many=True)
    tags = serializers.PrimaryKeyRelatedField(many=True, source='tag', queryset=Tag.objects.all())

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )


class RecipeSerializerForCart(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = (
            'recipe',
            'owner'
        )


class FavoriteRecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteRecipes
        fields = '__all__'
