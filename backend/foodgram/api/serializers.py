from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField

from rest_framework import serializers

from app.models import Recipe, Tag, Ingredient, Cart, FavoriteRecipes, IngredientAmount

from users.serializers import UserSerializer

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientAmountSerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(queryset=Ingredient.objects.all(),
                                        slug_field='name')
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        model = IngredientAmount
        fields = ('name', 'measurement_unit', 'amount')

    def get_measurement_unit(self, obj):
        return Ingredient.objects.get(name=obj.name.name).measurement_unit


class IngredientAmountSerializerWrite(IngredientAmountSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all(), source='name')

    class Meta(IngredientAmountSerializer.Meta):
        fields = ('id', 'amount')


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
            'cooking_time',
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
    ingredients = IngredientAmountSerializerWrite(many=True)
    tags = serializers.PrimaryKeyRelatedField(many=True, source='tag', queryset=Tag.objects.all())
    image = Base64ImageField()

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

    def create(self, validated_data):
        current_user = self.context['request'].user
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tag')
        recipe = Recipe.objects.create(author=current_user, **validated_data)

        for ingredient in ingredients_data:
            ing, _ = IngredientAmount.objects.get_or_create(
                **ingredient
            )
            recipe.ingredients.add(ing)

        for tag in tags_data:
            recipe.tag.add(tag)

        return recipe

    def update(self, instance, validated_data):
        recipe = instance

        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tag')
        query_set_ingredients = []
        query_set_tags = []

        for ingredient in ingredients_data:
            ing, _ = IngredientAmount.objects.get_or_create(**ingredient)
            query_set_ingredients.append(ing)

        for tag in tags_data:
            query_set_tags.append(tag)

        recipe.ingredients.set(query_set_ingredients)
        recipe.tag.set(query_set_tags)
        recipe.image = validated_data.get('image', recipe.image)
        recipe.name = validated_data.get('name', recipe.name)
        recipe.text = validated_data.get('text', recipe.text)
        recipe.cooking_time = validated_data.get('cooking_time', recipe.cooking_time)
        recipe.save()
        return recipe


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
