from rest_framework import serializers
from .models import * 


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']



class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'sku', 'name', 'description', 'price', 'category', 'category_name','created_at', 'updated_at']
        read_only_fields = ['id', 'sku', 'created_at', 'updated_at']

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be lower than 0.00")
        return value
    
    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Name cannot be empty")
        if len(value) > 255:
            raise serializers.ValidationError("Name too long")
        return value
    
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'sku', 'name',  'price']
        read_only_fields = ['id', 'sku']



