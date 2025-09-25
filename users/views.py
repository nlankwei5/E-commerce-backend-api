from django.shortcuts import render
from .serializer import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .models import * 


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

