from django.shortcuts import render
from cart.models import Cart, CartItem
from cart.serializers import CartSerializer, CartItemSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.generic import ListView


class CartDetail(APIView):

    def get_object(self, pk):
        try:
            return Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        cart = self.get_object(pk)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        cart = self.get_object(pk)
        serializer = CartSerializer(cart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        cart = self.get_object(pk)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartItemDetail(APIView):

    def get_object(self, pk):
        try:
            return CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        cart_item = self.get_object(pk)
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        cart_item = self.get_object(pk)
        serializer = CartItemSerializer(cart_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = CartItemSerializer(data=request.data)
        print(request.data)
        is_exist = CartItem.objects.filter(product=request.data.__getitem__('product')).exists()
        if is_exist:
            cart_item = CartItem.objects.get(product=request.data.__getitem__('product'))
            updated_data = request.data.copy()
            updated_data.__setitem__('quantity', cart_item.quantity + 1)
            serializer = CartItemSerializer(cart_item, data=updated_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            cart_item = CartItem.objects.get(pk=serializer.data.get('id'))
            cart = Cart.objects.get(pk=request.data.__getitem__('cart_id'))
            cart.items.add(cart_item)
            cart.save()
            print(cart.get_total_items())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        cart_item = self.get_object(pk)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartItemListView(ListView):
    model = CartItem
    paginate_by = 10
    template_name = "checkout.html"

    def get_context_data(self, **kwargs):
        context = super(CartItemListView, self).get_context_data(**kwargs)
        return context
