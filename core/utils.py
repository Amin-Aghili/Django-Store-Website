import json
from products.models import Product
from order.models import Order, OrderItem
from django.conf import settings


def cookie_cart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print('CART:', cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cart_items = order['get_cart_items']

    for i in cart:
        try:
            product = Product.objects.get(id=i)
            cart_items += cart[i]['quantity']
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                    'size': product.size,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total,
            }
            items.append(item)

            if product.digital is False:
                order['shipping'] = True
        except:
            pass
    print('CART ITEMS:', items)
    return {'cart_items': cart_items, 'order': order, 'items': items}


def cart_data(request):
    try:
        if request.user.is_authenticated:
            order, created = Order.objects.get_or_create(customer=request.user, complete=False)
            items = order.orderitem_set.all()
            cart_items = order.get_cart_items
        else:
            cookie_data = cookie_cart(request)
            cart_items = cookie_data['cart_items']
            order = cookie_data['order']
            items = cookie_data['items']
        return {'cart_items': cart_items, 'order': order, 'items': items}
    except:
        pass


def guest_order(request, data):
    print('User is not logged in')

    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookie_data = cookie_cart(request)
    items = cookie_data['items']

    customer, created = settings.AUTH_USER_MODEL.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        order = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'],
        )

    return customer, order
