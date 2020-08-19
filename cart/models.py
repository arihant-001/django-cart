from django.db import models
from catalog.models import Product


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    date_added = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField(default=1)
    cart_id = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    def get_price(self):
        return self.quantity*self.product.price

    def get_name(self):
        return self.product.name


class Cart(models.Model):
    items = models.ManyToManyField(CartItem)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.product.price for item in self.items.all()])

    def get_total_items(self):
        return sum([item.quantity for item in self.items.all()])
