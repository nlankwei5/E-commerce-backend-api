from rest_framework import serializers
from .models import Cart, CartItem
from catalog.serializers import SimpleProductSerializer
from catalog.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(many = False)
    sub_total = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'sub_total']

    def get_sub_total(self, obj):
        return obj.product.price * obj.quantity


class CartSerializer(serializers.ModelSerializer): 
    items = CartItemSerializer(many=True)
    grand_total = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'updated_at', 'items', 'grand_total']
        read_only_fields = ['id','created_at', 'updated_at']

    def get_grand_total(self, obj):
        items = obj.items.all()
        total = sum([item.quantity * item.product.price for item in items ])
        return total 
        
        
class AddCartItemSerializer(serializers.ModelSerializer):
    product_sku = serializers.CharField(write_only=True)
    product_sku_out = serializers.SerializerMethodField(read_only=True)
    

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_sku = self.validated_data['product_sku']
        quantity = self.validated_data['quantity']


        try:
            product = Product.objects.get(sku=product_sku)
        except Product.DoesNotExist:
            raise serializers.ValidationError({"product_sku": "Invalid product SKU"})
        try:
            cartitems = CartItem.objects.get(product=product, cart_id=cart_id)
            cartitems.quantity += quantity
            cartitems.save()
            self.instance = cartitems
        except:
            self.instance = CartItem.objects.create(product=product, cart_id=cart_id, quantity=quantity)

        return self.instance
    
    class Meta:
        model = CartItem
        fields = ['id', 'product_sku', 'product_sku_out', 'quantity']
    
    def get_product_sku_out(self, obj):
        return obj.product.sku

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta: 
        model = CartItem
        fields = ['quantity']
