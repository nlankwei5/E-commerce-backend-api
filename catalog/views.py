from django.shortcuts import render
from rest_framework import viewsets
from .serializers import * 
from rest_framework.response import Response
from rest_framework import filters
from .models import * 
from django_filters.rest_framework import DjangoFilterBackend



# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'sku'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category','category__name', 'price', 'created_at']
    search_fields = ['name']
    ordering_fields = ['price']




