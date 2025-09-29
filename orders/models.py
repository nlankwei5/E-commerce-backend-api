from django.db import models
from users.models import User
from catalog.models import Product

# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.ForeignKey(Product.price, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def save(self, *args, **kwargs):
        if CartItem.objects.filter(cart=self.cart, product=self.product).exists():
            existing_item = CartItem.objects.get(cart=self.cart, product=self.product)
            existing_item.quantity += self.quantity
            existing_item.save()
        return super().save(*args, **kwargs)

    




