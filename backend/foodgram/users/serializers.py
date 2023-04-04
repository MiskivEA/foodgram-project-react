from django.contrib.auth import get_user_model

from rest_framework import serializers
from djoser.serializers import (UserSerializer as BaseUserSerializer,
                                UserCreateSerializer as BaseUserCreateSerializer,
                                SetPasswordSerializer as BaseSetPasswordSerializer,
                                )
from users.models import Follow

User = get_user_model()


class UserSerializer(BaseUserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        current_user = self.context['request'].user
        if self.context['request'].user.is_anonymous:
            return False
        return Follow.objects.filter(user=current_user, author=obj).exists()


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'password')


class SetPasswordSerializer(BaseSetPasswordSerializer):
    class Meta():
        fields = ('new_password', 'current_password')


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'
