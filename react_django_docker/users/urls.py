from django.contrib import admin
from django.urls import path
from . import views
from users.views import (
    LogoutUser,
    UserView,
    UserLogin,
    AuthenticationUser,
    PermissionAPIView,
    RoleViewSet,
    UserGenericAPIView
)
urlpatterns = [
    path('user', UserView.as_view()),
    path('login', UserLogin.as_view()),
    path('user_authentication', AuthenticationUser.as_view()),
    path('logout', LogoutUser.as_view()),
    path('permission', PermissionAPIView.as_view()),
    path('roles', RoleViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('roles/<str:pk>', RoleViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'        
    })),
    path('user/<int:pk>', UserGenericAPIView.as_view())
]