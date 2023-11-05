from django.shortcuts import render
from django.contrib.auth import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class User(APIView):

    def get(self, request):
        return Response({'message': 'success'})