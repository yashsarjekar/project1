from django.shortcuts import render
from rest_framework import generics, status
# Create your views here.
from rest_framework.response import Response
from users.authenticate import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from users.constants import *
import csv
from rest_framework.views import APIView
from react_django_docker.pagination import CustomPagination
from orders.services.order_services.order_services import OrderService

class OrderGenericAPIView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self):
        self.__order_service = OrderService()
        self.__custom_pagination = CustomPagination()

    def get(self, requests):

        page_number = self.request.query_params.get('page_number', None)
        orders = self.__order_service. \
            get_all_records()
        order_data = []
        if page_number:
            page_number = int(page_number)
            page_size = PAGE_SIZE
            recods, has_next = self.__custom_pagination.get_paginated_data(
                data=orders,
                page_number=page_number,
                page_size=page_size
            )
            for recod in recods:
                order_data.append({
                    "first_name": recod.get_first_name(),
                    "last_name": recod.get_last_name(),
                    "email": recod.get_email(),
                    "order_items": recod.get_order_items(),
                    "total_price": recod.get_total_price(),
                    "created_at": recod.get_created_at(),
                    "updated_at": recod.get_updated_at()
                })
            API_RESPONSE['meta'] = {
                'message': 'success',
                'total_records': len(orders),
                'total_pages': self.__custom_pagination.total_pages(orders, page_size),
                'current_page_number': page_number
            }
        else:
            for recod in orders:
                order_data.append({
                    "first_name": recod.get_first_name(),
                    "last_name": recod.get_last_name(),
                    "email": recod.get_email(),
                    "order_items": recod.get_order_items(),
                    "total_price": recod.get_total_price(),
                    "created_at": recod.get_created_at(),
                    "updated_at": recod.get_updated_at()
                })
        API_RESPONSE['results'] = order_data

        return Response(
            API_RESPONSE,
            status=status.HTTP_200_OK
        )


class ExportOrders(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def __init__(self):
        self.__order_service = OrderService()

    def get(self, requests):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=orders.csv'

        orders = self.__order_service. \
            get_all_records()

        writer = csv.writer(response)
        writer.writerow(
            [
                'first_name',
                'last_name',
                'email',
                'order_items',
                'total_price',
                'created_at',
                'updated_at'
            ]
        )

        for order in orders:
            writer.writerow(
                [
                    order.get_first_name(),
                    order.get_last_name(),
                    order.get_email(),
                    order.get_order_items(),
                    order.get_total_price(),
                    order.get_created_at(),
                    order.get_updated_at()
                ])

        return response


