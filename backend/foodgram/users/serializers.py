from app.models import Recipe
from django.contrib.auth import get_user_model
from djoser.serializers import \
    SetPasswordSerializer as BaseSetPasswordSerializer
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers

from users.models import Follow

User = get_user_model()


class UserSerializer(BaseUserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        current_user = self.context.get('request').user
        if current_user.is_anonymous:
            return False
        return Follow.objects.filter(user=current_user, author=obj).exists()


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ('id', 'email', 'username',
                  'first_name', 'last_name', 'password')


class RecipeSerializerSubs(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class UserSerializerSubscribe(UserSerializer):
    """Сериализатор пользователя для подписок (read only)"""
    recipe_count = serializers.SerializerMethodField()
    recipes = RecipeSerializerSubs(read_only=True, many=True)

    class Meta(UserSerializer.Meta):
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipe_count')

    def get_recipe_count(self, obj):
        return obj.recipes.all().count()


class SetPasswordSerializer(BaseSetPasswordSerializer):
    class Meta():
        fields = ('new_password', 'current_password')


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'
