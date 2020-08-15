from django.db import models
from catalog.models import Product
from django.contrib.auth.models import User


class CartItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, null=False)
    date_added = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField(default=1)
    cart_id = models.IntegerField(null=True)

    def __str__(self):
        return self.product.name


class Cart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    items = models.ManyToManyField(CartItem)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.product.price for item in self.items.all()])

    def get_total_items(self):
        return sum([item.quantity for item in self.items.all()])
