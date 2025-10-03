from django.shortcuts import render
from rest_framework import viewsets 
from .models import Cart, CartItem
from .serializer import CartSerializer, AddCartItemSerializer, CartItemSerializer, UpdateCartItemSerializer

# Create your views here.

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemsViewSet(viewsets.ModelViewSet):

    http_method_names = ['get', 'post', 'patch', 'delete']
    
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    
