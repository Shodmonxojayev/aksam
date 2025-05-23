from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Product(models.Model):
    product_name = models.CharField(max_length=50, null=True)
    product_description = models.TextField(max_length=170, null=True)
    product_price = models.SmallIntegerField(null=True)

    def __str__(self):
        return self.product_name


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price_per_item = models.IntegerField()

    def total_price(self):
        return self.quantity * self.price_per_item


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Можно добавить поле session_key, если хочешь привязывать корзину к сессии для неавторизованных

    def __str__(self):
        return f"Cart {self.id} for {self.user or 'Anonymous'}"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.product_price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name}"
