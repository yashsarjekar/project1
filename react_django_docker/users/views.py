from typing import Any
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from users.services.user_services.\
user_services import UserService
from users.serializers import (
    UserSerializer,
    PermissionSerializer,
    RoleSerializer
)
from users.constants import *
from users.authenticate import generate_user_token
from rest_framework.permissions import IsAuthenticated
from users.authenticate import JWTAuthentication
from rest_framework import exceptions, viewsets, status, generics
from react_django_docker.pagination import CustomPagination

# Create your views here.
class UserView(APIView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.__user_service = UserService()
        self.__custom_paginaton = CustomPagination()

    def get(self, request):
        page_number = int(self.request.query_params.get('page_number', None))
        users = self.__user_service.\
        get_all_records()
        page_size = PAGE_SIZE
        recods, has_next = self.__custom_paginaton.get_paginated_data(
            data=users,
            page_number=page_number,
            page_size=page_size
        )
        user_serializer = UserSerializer(recods, many=True)
        API_RESPONSE['results'] = user_serializer.data
        API_RESPONSE['meta'] = {
            'message': 'success',
            'total_records': len(users),
            'total_pages': len(users) // page_size,
            'current_page_number': page_number
        }
        return Response(
            API_RESPONSE,
            status=status.HTTP_200_OK
        )
    
    def post(self, request):
        data = request.data

        if data['password'] != data['passsword_confirm']:
            raise Exception('Passwords do not match')
        

        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class UserLogin(APIView):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.__user_service = UserService()

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = self.__user_service.authenticate_user_login(
            email=email
        )
        msg = 'User successfully login'
        user_login = True

        if email is None:
            msg = 'Please provide email!'
            user_login = False
        elif password is None:
            msg = 'Please provide password!'
            user_login = False
        elif user is None:
            msg = 'User does not exist!'
            user_login = False
        elif not user.check_password(password):
            msg = 'Incorrect password !'
            user_login = False
        response = Response()
        API_RESPONSE['message'] = msg
        token = generate_user_token(user=user)
        if user_login:
            response.set_cookie(key='jwt', value=token, httponly=True)
            API_RESPONSE['results'] = {
                'jwt': token
            }
        response.data = API_RESPONSE
        return response
    
class AuthenticationUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_serializer = UserSerializer(request.user)
        API_RESPONSE['results'] = user_serializer.data
        return Response(API_RESPONSE)
    

class LogoutUser(APIView):
    def post(self, request):
        response =  Response()
        response.delete_cookie(key='jwt')
        response.data = {
            'message': 'success'
        }

        return response
    

class PermissionAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.__user_service = UserService()

    def get(self, request):
        permission_serializer = PermissionSerializer(
            self.__user_service.get_all_permission(),
            many=True
        )
        API_RESPONSE['results'] = permission_serializer.data
        API_RESPONSE['message'] = 'List of all permission'
        return Response(
            API_RESPONSE
        )


class RoleViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.__user_services = UserService()

    def list(self, request):
        serializer = RoleSerializer(
            self.__user_services.get_all_roles(),
            many=True
        )
        API_RESPONSE['results'] = serializer.data
        API_RESPONSE['message'] = 'List of all roles'
        return Response(API_RESPONSE)

    def create(self, request):
        serializer = RoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        API_RESPONSE['results'] = serializer.data
        return Response(
            API_RESPONSE,
            status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, pk=None):
        role = self.__user_services.get_role(id=pk)
        serializer = RoleSerializer(role)

        API_RESPONSE['results'] = serializer.data

        return Response(
            API_RESPONSE
        )
        

    def update(self, request, pk=None):
        role = self.__user_services.get_role(id=pk)
        serializer = RoleSerializer(instance=role, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        API_RESPONSE['results'] = serializer.data
        return Response(
            API_RESPONSE,
            status=status.HTTP_202_ACCEPTED
        )

    def destroy(self, request, pk=None):
        self.__user_services.delete_role(id=pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class  UserGenericAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.__user_services = UserService()

    def get(self, request, pk=None):
        if pk:
            user_record = self.__user_services.\
                get_user_details(
                id=pk
            )
            user_serializer = UserSerializer(user_record)
            API_RESPONSE['results'] = user_serializer.data
            return Response(
                API_RESPONSE,
                status=status.HTTP_200_OK
            )
        else:
            API_RESPONSE['message'] = 'Not a valid user'
            return Response(
                API_RESPONSE,
                status=status.HTTP_404_NOT_FOUND
            )
        
    def put(self, request, pk=None):
        if pk:
            pass