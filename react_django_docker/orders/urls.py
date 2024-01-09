from django.contrib import admin
from django.urls import path
from orders.views import OrderGenericAPIView, ExportOrders

urlpatterns = [
    path('orders', OrderGenericAPIView.as_view()),
    path('orders/<int:pk>', OrderGenericAPIView.as_view()),
    path('export', ExportOrders.as_view()),
]