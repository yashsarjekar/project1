from django.shortcuts import render
from rest_framework import generics, status
# Create your views here.
from rest_framework.response import Response
from users.authenticate import JWTAuthentication
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from products.services.product_services.product_services import ProductService
from users.constants import *
from products.serializers import ProductSerializer
from react_django_docker.pagination import CustomPagination
from django.core.files.storage import default_storage


class ProductGenericAPIView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, )

    def get(self, requests):
        product_service = ProductService()
        custom_paginaton = CustomPagination()
        page_number = self.request.query_params.get('page_number', None)
        products = product_service. \
            get_all_records()
        if page_number:
            page_number = int(page_number)
            page_size = PAGE_SIZE
            recods, has_next = custom_paginaton.get_paginated_data(
                data=products,
                page_number=page_number,
                page_size=page_size
            )
            product_serializer = ProductSerializer(recods, many=True)
            API_RESPONSE['meta'] = {
                'message': 'success',
                'total_records': len(products),
                'total_pages': custom_paginaton.total_pages(products, page_size),
                'current_page_number': page_number
            }
        else:
            product_serializer = ProductSerializer(products, many=True)
        API_RESPONSE['results'] = product_serializer.data

        return Response(
            API_RESPONSE,
            status=status.HTTP_200_OK
        )

    def post(self, requests):
        title = requests.data.get('title')
        description = requests.data.get('description')
        file = requests.FILES.get('image')
        price = requests.data.get('price')
        file_name = default_storage.save(file.name, file)
        url = default_storage.url(file_name)

        data = {
            "title": title,
            "description": description,
            "image": url,
            "price": price
        }

        serializer = ProductSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)