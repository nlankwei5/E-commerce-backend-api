from django.shortcuts import render
from rest_framework import viewsets
from .serializers import * 
from rest_framework.response import Response
from .models import * 



# Create your views here.
class CategoryViewset(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CatergorySerializer



class ProductViewset(viewsets.ReadOnlyModelViewSet):

    queryset = Product.objects.all()
    serializer_class = Product 

    
