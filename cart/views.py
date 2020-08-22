from cart.models import Cart, CartItem, Order, OrderItem, ShippingAddress
from catalog.models import Product
from cart.serializers import CartSerializer, CartItemSerializer
from django.shortcuts import render
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import datetime


class CartView(APIView):

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


def cart_item_exist(serializer):
    return CartItem.objects.filter(
        product=serializer.validated_data['product'],
        cart_id=serializer.validated_data['cart_id']
    ).exists()


def update_cart_quantity(request):
    data = json.loads(request.body.decode('utf-8'))
    product_id = data['product_id']
    action = data['action']

    product = Product.objects.get(id=product_id)
    cart_user = request.user.cartuser
    order, created = Order.objects.get_or_create(user=cart_user, complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        order_item.quantity += 1
    elif action == 'sub':
        order_item.quantity -= 1

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Item added', safe=False, status=status.HTTP_200_OK)


def get_cart_item_by_product_and_cart_id(serializer):
    return CartItem.objects.get(
        product=serializer.data['product'],
        cart_id=serializer.data['cart_id'])


class CartItemView(APIView):

    def get_object(self, pk):
        try:
            return CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        cart_item = self.get_object(pk)
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        cart_item = self.get_object(pk)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def cart_details(request):
    if request.user.is_authenticated:
        cart_user = request.user.cartuser
        print(cart_user.email)
        order, created = Order.objects.get_or_create(user=cart_user, complete=False)
        # print(order.get_total)
        items = order.orderitem_set.all()
        print(items)
    else:
        items = []
        order = {
            'get_total_price': 0,
            'get_total_quantity': 0
        }
    context = {'cart_items': items, 'order': order}
    return render(request, 'cart/cart_detail.html', context)


def checkout(request):
    if request.user.is_authenticated:
        cart_user = request.user.cartuser
        print(cart_user.email)
        order, created = Order.objects.get_or_create(user=cart_user, complete=False)
        items = order.orderitem_set.all()
        print(items)
    else:
        items = []
        order = {
            'get_total_price': 0,
            'get_total_quantity': 0
        }
    context = {'cart_items': items, 'order': order}
    return render(request, 'cart/checkout.html', context=context)


def get_cart_quantity(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            cart_user = request.user.cartuser
            order, created = Order.objects.get_or_create(user=cart_user, complete=False)
            quantity = order.get_total_quantity
        else:
            quantity = 0
        data = {'quantity': quantity}
        return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

    return JsonResponse("error", safe=False, status=status.HTTP_400_BAD_REQUEST)


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body.decode('utf-8'))
    print(data)
    if request.user.is_authenticated:
        cart_user = request.user.cartuser
        order, created = Order.objects.get_or_create(user=cart_user, complete=False)
        total = data['user']['total']
        order.transaction_id = transaction_id
        if total == order.get_total_price:
            order.complete = True
        order.save()

        ShippingAddress.objects.create(
            user=cart_user,
            order=order,
            address=data['ship-info']['address'],
            city=data['ship-info']['city'],
            state=data['ship-info']['state'],
            zipcode=data['ship-info']['zipcode'],
        )
    return JsonResponse('Payment Complete', safe=False)
