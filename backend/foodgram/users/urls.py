from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, FollowViewSet

app_name = 'users'

router_v1 = DefaultRouter()

router_v1.register(r'users/subscriptions', FollowViewSet, basename='subscriptions')
router_v1.register(r'users', UserViewSet)


urlpatterns = [
    path('api', include(router_v1.urls)),
    path('api', include('djoser.urls')),
    path('api/auth', include('djoser.urls.authtoken')),
]