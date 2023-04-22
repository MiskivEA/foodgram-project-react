from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as BaseUserViewSet
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.custom_utils import LimitOffsetPagination
from users.models import Follow
from users.serializers import UserSerializer, UserSerializerSubscribe

User = get_user_model()


class FollowViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    serializer_class = UserSerializerSubscribe

    def get_queryset(self):
        follows = Follow.objects.filter(user=self.request.user)
        return follows


class UserViewSet(BaseUserViewSet):
    pagination_class = LimitOffsetPagination
    serializer_class = UserSerializer
    permission_classes = permissions.IsAuthenticatedOrReadOnly,

    @action(methods=['get'],
            detail=False,
            pagination_class=LimitOffsetPagination)
    def subscriptions(self, request):
        follows = Follow.objects.filter(user=request.user)
        page = self.paginate_queryset(follows)
        if page is not None:
            serializer = UserSerializerSubscribe(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = UserSerializerSubscribe(follows, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post', 'delete'],
            detail=True)
    def subscribe(self, request, **kwargs):
        user = request.user
        id_user_to_follow = kwargs['id']
        author = get_object_or_404(User, pk=id_user_to_follow)
        serializer = UserSerializerSubscribe(author,
                                             context={'request': request})

        if request.method == 'POST':
            follow_obj, created = Follow.objects.get_or_create(user=user,
                                                               author=author)
            if created:
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response({'error': 'Ошибка подписки'},
                            status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            follow = Follow.objects.filter(user=user, author=author).exists()
            if follow:
                Follow.objects.get(user=user, author=author).delete()
                return Response({'Вы отписались от пользователя'},
                                status=status.HTTP_200_OK)
            return Response({'error': 'Вы не были подписаны'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
