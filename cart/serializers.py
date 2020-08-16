from rest_framework import serializers
from cart.models import Cart, CartItem


class CartSerializer(serializers.ModelSerializer):
    quantity = serializers.CharField(source='get_total_items', read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'owner', 'items', 'quantity']


class CartItemSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField(source='get_price', read_only=True)
    name = serializers.CharField(source='get_name', read_only=True)

    class Meta:
        model = CartItem
        fields = ['name', 'id', 'product', 'quantity', 'price']
