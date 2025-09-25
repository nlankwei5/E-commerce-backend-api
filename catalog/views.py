from django.shortcuts import render
from rest_framework import viewsets
from .serializers import * 
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import filters
from .models import * 
from django_filters.rest_framework import DjangoFilterBackend



# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.action in ['create','update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.select_related('category')
    serializer_class = ProductSerializer
    lookup_field = 'sku'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'price', 'created_at']
    search_fields = ['name']
    ordering_fields = ['price']
    permission_classes = [AllowAny]




