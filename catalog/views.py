from django.shortcuts import render
from rest_framework import viewsets
from .serializers import * 
from rest_framework.response import Response
from rest_framework import filters
from .models import * 
from django_filters.rest_framework import DjangoFilterBackend



# Create your views here.
class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CatergorySerializer



class ProductViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'sku'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'price', 'created_at']
    search_fields = ['name']
    ordering_fields = ['price']



    def list(self, request):
        products = Product.objects.all()
        serializers = self.get_serializer(products, many=True)
        return Response(serializers.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializers = self.get_serializer(instance)
        return Response(serializers.data)



