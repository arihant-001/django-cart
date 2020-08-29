from catalog.models import Product
from cart.models import Order, OrderItem, ShippingAddress
from user.models import CartUser
import json


def get_cookie_cart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {
        'get_total_price': 0,
        'get_total_quantity': 0
    }

    for i in cart:
        try:
            order['get_total_quantity'] += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])
            order['get_total_price'] += total
            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'image_url': product.image_url,
                    'get_absolute_url': product.get_absolute_url,
                },
                'quantity': cart[i]['quantity'],
                'get_total_price': total
            }
            items.append(item)
        except:
            pass

    return {'cart_items': items, 'order': order}


def get_cart_data(request):
    if request.user.is_authenticated:
        cart_user = request.user.cartuser
        print(cart_user.email)
        order, created = Order.objects.get_or_create(user=cart_user, complete=False)
        items = order.orderitem_set.all()
        print(items)
    else:
        cookie_cart = get_cookie_cart(request)
        order = cookie_cart['order']
        items = cookie_cart['cart_items']

    return {'cart_items': items, 'order': order}


def get_guest_order(request, data):
    print('Not logged in user')
    name = data['user-info']['name']
    email = data['user-info']['email']
    cookie_cart = get_cookie_cart(request)
    items = cookie_cart['cart_items']

    cart_user = CartUser.objects.create(
        name=name,
        email=email
    )
    cart_user.save()

    order = Order.objects.create(
        user=cart_user,
        complete=False,
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    return cart_user, order


def get_orders_data(request):
    if request.user.is_authenticated:
        cart_user = request.user.cartuser
        orders = Order.objects.filter(user=cart_user, complete=True)
        orders_list = []
        for order in orders:
            items = []
            order_items = order.orderitem_set.all()
            for order_item in order_items:
                product = Product.objects.get(id=order_item.product.id)
                item = {
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'image_url': product.image_url,
                        'get_absolute_url': product.get_absolute_url,
                    },
                    'quantity': order_item.quantity,
                    'get_total_price': order_item.get_total_price
                }
                items.append(item)

            ship_address = ShippingAddress.objects.get(order=order)
            order = {
                'transaction_id': order.transaction_id,
                'get_total_price': order.get_total_price,
                'get_total_quantity': order.get_total_quantity,
                'date_ordered': order.date_ordered,
                'address': ship_address,
                'items': items
            }
            orders_list.append(order)

    else:
        orders_list = []

    return {'orders_list': orders_list}
