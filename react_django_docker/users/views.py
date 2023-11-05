from typing import Any
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from users.services.user_services.\
user_services import UserService
# Create your views here.
class UserView(APIView):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.__user_service = UserService()

    def get(self, request):
        users = self.__user_service.\
        get_all_records()
        return Response(
            {
                'message': 'success',
                'users': users
            }
        )