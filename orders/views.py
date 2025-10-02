from django.shortcuts import render
from rest_framework import viewsets 
from .models import Cart, CartItem
from .serializer import CartSerializer, AddCartItemSerializer, CartItemSerializer

# Create your views here.

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemsViewSet(viewsets.ModelViewSet):
    
    def get_queryset(self):
        return CartItem.objects.filter(id=self.kwargs['cart_pk'])

    

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    
