from django.contrib import admin
from django.urls import path
from products.views import (
    ProductGenericAPIView
)
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('products', ProductGenericAPIView.as_view()),
    path('products/<int:pk>', ProductGenericAPIView.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)