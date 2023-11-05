from django.contrib import admin
from django.urls import path
from views import User

urlpatterns = [
    path('api/v1/user', User.as_view()),
]