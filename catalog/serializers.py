from rest_framework import serializers
from .models import * 


class CatergorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']



class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'sku', 'name', 'description', 'price', 'category_name','created_at', 'updated_at']
        read_only_fields = ['id', 'sku', 'created_at', 'updated_at']




