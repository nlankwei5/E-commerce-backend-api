from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# Create your models here.

class CustomAccountManager(BaseUserManager):
    
    def create_user(self, email, username, first_name, last_name, password, **other_fields):
        
        if not email: 
            raise ValueError('You must provide email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name, last_name=last_name, **other_fields) 
        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, email, username, first_name, last_name, password, **other_fields):
        
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True')
        
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True')
        
        return self.create_user(email, username, first_name, last_name, password, **other_fields)
        





class User(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField (max_length=30, unique=True, blank=False)
    email = models.EmailField(unique=True, blank=False)
    first_name= models.CharField(max_length=100)
    last_name= models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects= CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.username
