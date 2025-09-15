import random 
import string
from django.db import models
from django.utils.text import slugify


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)


    def save(self, *args, **kwargs):
         self.slug = slugify(self.name)
         return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    sku = models.CharField(max_length=30, unique=True, null=True, blank=True)
    name = models.CharField(max_length= 50, blank= False)
    description = models.CharField (max_length= 100, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.ForeignKey(Category, on_delete= models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    
    def generate_sku(self):
        random_part = ''.join(random.choices(string.digits, k=6))

        return f"{self.category.slug.upper()}-{random_part}"
    
    def save(self, *args, **kwargs):
        if not self.sku:
            new_sku = self.generate_sku()
        else:
             return
        while Product.objects.filter(sku=new_sku).exists():  
                new_sku = self.generate_sku()
        self.sku = new_sku
        return super().save(*args, **kwargs)

    
    def __str__(self):
        return self.name