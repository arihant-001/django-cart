from django.db import models
from catalog.models import Product
from user.models import CartUser


class Order(models.Model):
    user = models.ForeignKey(CartUser, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_total_price(self):
        return sum([item.get_total_price for item in self.orderitem_set.all()])

    @property
    def get_total_quantity(self):
        return sum([item.quantity for item in self.orderitem_set.all()])


class ShippingAddress(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(CartUser, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.address


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.product.name

    @property
    def get_total_price(self):
        return self.product.price*self.quantity

