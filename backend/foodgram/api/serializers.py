from django.contrib.auth import get_user_model

from rest_framework import serializers

from app.models import Recipe, Tag, Ingredient, Cart, FavoriteRecipes, IngredientAmount
from users.serializers import UserSerializer

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientAmountSerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(queryset=Ingredient.objects.all(),
                                        slug_field='name', required=False)

    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_measurement_unit(self, obj):
        # print(obj.name.name)
        ms = Ingredient.objects.filter(name=obj.name.name).first()
        # print(ms)
        return ms.measurement_unit


# class IngredientRecipeSerializerWrite(serializers.Serializer):
#     id = serializers.IntegerField()
#     amount = serializers.IntegerField(required=True)
#
#     def create(self, validated_data):
#         ingredient_id = validated_data['id']
#         ingredient = Ingredient.objects.get(pk=ingredient_id)
#         measurement_unit = MeasurementUnit.objects.get()
#         print(ingredient.name, ingredient.measurement_unit, validated_data['amount'], sep='\n')
#
#         return IngredientRecipe.objects.create(
#             name=ingredient,
#             measurement_unit=ingredient.measurement_unit,
#             amount=validated_data['amount']
#         )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientAmountSerializer(many=True, read_only=True)
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
    ingredients = IngredientAmountSerializer(many=True)
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
