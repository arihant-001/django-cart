from rest_framework import serializers
from cart.models import Cart, CartItem


class CartSerializer(serializers.ModelSerializer):
    quantity = serializers.CharField(source='get_total_items', read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'owner', 'items', 'quantity']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']
