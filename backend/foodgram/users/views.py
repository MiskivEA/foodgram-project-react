from django.contrib.auth import get_user_model
from django.http import JsonResponse, FileResponse
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from djoser.views import UserViewSet as BaseUserViewSet


from users.models import Follow
from users.serializers import FollowSerializer, UserSerializer, UserSerializerSubscribe


User = get_user_model()


class CustomPaginationClass(PageNumberPagination):
    page_size = 5


class FollowViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPaginationClass
    serializer_class = UserSerializerSubscribe

    def get_queryset(self):
        follows = Follow.objects.filter(user=self.request.user)
        return [follow.author for follow in follows]


class UserViewSet(BaseUserViewSet):
    pagination_class = CustomPaginationClass
    serializer_class = UserSerializer

    @action(methods=['post', 'delete'],
            detail=True)
    def subscribe(self, request, **kwargs):
        user = request.user
        id_user_to_follow = kwargs['id']
        author = get_object_or_404(User, pk=id_user_to_follow)
        serializer = UserSerializerSubscribe(author)

        if request.method == 'POST':
            follow_obj, flag_created = Follow.objects.get_or_create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'DELETE':
            get_object_or_404(Follow, user=user, author=author).delete()
            return Response({f'Вы отписались от пользователя {author.email}'}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


