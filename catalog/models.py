import random 
import string
from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField
from cloudinary.utils import cloudinary_url



# Create your models here.

def validate_price(value):
        if value < 0:
            raise ValidationError('Price cannot be less than $0.00')

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, unique=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    sku = models.CharField(max_length=30, unique=True, null=True, blank=True)
    name = models.CharField(max_length= 50, blank= False)
    description = models.TextField (blank=True)
    image = CloudinaryField('file', resource_type="raw", allowed_formats=['jpg'], blank=False, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, validators=[validate_price])
    category = models.ForeignKey(Category, on_delete= models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def generate_sku(self):
        random_part = ''.join(random.choices(string.digits, k=6))

        return f"{self.category.slug.upper()}-{random_part}"
    
    
    def save(self, *args, **kwargs):
        if not self.sku:
            new_sku = self.generate_sku()
            while Product.objects.filter(sku=new_sku).exists():  
                    new_sku = self.generate_sku()
            self.sku = new_sku
        return super().save(*args, **kwargs)

    
    def __str__(self):
        return f"{self.sku} - {self.name}"
    
    class Meta:
        indexes = [
            models.Index(fields=["sku"]),        
            models.Index(fields=["name"]),       
            models.Index(fields=["price"]),      
            models.Index(fields=["category"]),   
        ]

