from django.contrib.auth import get_user_model

from rest_framework import serializers
from djoser.serializers import (UserSerializer as BaseUserSerializer,
                                UserCreateSerializer as BaseUserCreateSerializer,
                                SetPasswordSerializer as BaseSetPasswordSerializer,
                                )
from app.models import Recipe, Tag, Ingredient, Cart, Follow, FavoriteRecipes, IngredientsAmount

User = get_user_model()


class UserSerializer(BaseUserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        fields = ['email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed']

    def get_is_subscribed(self, obj):
        current_user = self.context['request'].user
        if self.context['request'].user.is_anonymous:
            return False
        return Follow.objects.filter(user=current_user, author=obj).exists()


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'password']


class SetPasswordSerializer(BaseSetPasswordSerializer):
    class Meta():
        fields = ['new_password', 'current_password']


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientsAmountSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = IngredientsAmount
        fields = (
            'ingredient',
            'amount'
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientsAmountSerializer(many=True)
    tags = TagSerializer(many=True, source='tag')
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


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'


class FavoriteRecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteRecipes
        fields = '__all__'


