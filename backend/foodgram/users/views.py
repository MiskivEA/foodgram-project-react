from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from djoser.views import UserViewSet as BaseUserViewSet

from api.custom_utils import CustomPaginationClass
from users.models import Follow
from users.serializers import UserSerializer, UserSerializerSubscribe

User = get_user_model()


class FollowViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPaginationClass
    serializer_class = UserSerializerSubscribe

    def get_queryset(self):
        follows = Follow.objects.filter(user=self.request.user)
        return [follow.author for follow in follows]


class UserViewSet(BaseUserViewSet):
    pagination_class = CustomPaginationClass
    serializer_class = UserSerializer
    filter_backends = DjangoFilterBackend,
    filterset_fields = 'is_subscribed',

    @action(methods=['post', 'delete'],
            detail=True)
    def subscribe(self, request, **kwargs):
        user = request.user
        id_user_to_follow = kwargs['id']
        author = get_object_or_404(User, pk=id_user_to_follow)
        serializer = UserSerializerSubscribe(author, context={'request': request})

        if request.method == 'POST':
            follow_obj, created = Follow.objects.get_or_create(user=user, author=author)
            if created:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'error': 'Ошибка подписки'}, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            get_object_or_404(Follow, user=user, author=author).delete()
            return Response({f'Вы отписались от пользователя {author.email}'}, status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
