from cart.models import Order, OrderItem, ShippingAddress
from catalog.models import Product
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
import json
import datetime
from . utils import get_cart_data, get_guest_order


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


def cart_details(request):
    return render(request, 'cart/cart_detail.html', get_cart_data(request))


def checkout(request):
    return render(request, 'cart/checkout.html', context=get_cart_data(request))


def get_cart_quantity(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            cart_user = request.user.cartuser
            order, created = Order.objects.get_or_create(user=cart_user, complete=False)
            quantity = order.get_total_quantity
        else:

            try:
                cart = json.loads(request.COOKIES['cart'])
            except:
                cart = {}

            quantity = 0
            for i in cart:
                quantity += cart[i]['quantity']
        data = {'quantity': quantity}
        return JsonResponse(data, safe=False, status=status.HTTP_200_OK)

    return JsonResponse("error", safe=False, status=status.HTTP_400_BAD_REQUEST)


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    print(request.body)
    data = json.loads(request.body.decode('utf-8'))
    print(data)
    if request.user.is_authenticated:
        cart_user = request.user.cartuser
        order, created = Order.objects.get_or_create(user=cart_user, complete=False)
    else:
        cart_user, order = get_guest_order(request, data)
    ShippingAddress.objects.create(
        user=cart_user,
        order=order,
        address=data['ship-info']['address'],
        city=data['ship-info']['city'],
        state=data['ship-info']['state'],
        zipcode=data['ship-info']['zipcode'],
    )
    order.transaction_id = transaction_id
    order.complete = True
    order.save()
    return JsonResponse('Payment Complete', safe=False)
