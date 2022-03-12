from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
import json
import datetime
from .models import *


class StoreView(View):
    products = Product.objects.all()
    template_name = 'store/store.html'

    def get(self, request):
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0}
            cartItems = order['get_cart_items']
        context = {'products': self.products, 'cartItems': cartItems, 'shipping': False}
        return render(request, self.template_name, context)

    def post(self, request):
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0}
            cartItems = order['get_cart_items']
        context = {'products': self.products, 'cartItems': cartItems, 'shipping': False}
        return render(request, self.template_name, context)


class CartView(View):
    template_name = 'store/cart.html'

    def get(self, request):
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            try:
                cart = json.loads(request.COOKIES['cart'])
            except:
                cart = {}
            print('CART:', cart)
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
            cartItems = order['get_cart_items']

            for i in cart:
                cartItems += cart[i]['quantity']

                product = Product.objects.get(id=i)
                total = (product.price * cart[i]['quantity'])

                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']

                item = {
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'imageURL': product.imageURL,
                    },
                    'quantity': cart[i]['quantity'],
                    'get_total': total,
                }
                items.append(item)


        context = {'items': items, 'order': order, 'cartItems': cartItems, 'shipping': False}
        return render(request, self.template_name, context)

    def post(self, request):
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            try:
                cart = json.loads(request.COOKIES['cart'])
            except:
                cart = {}
            print('CART:', cart)
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
            cartItems = order['get_cart_items']

            for i in cart:
                cartItems += cart[i]['quantity']

                product = Product.objects.get(id=i)
                total = (product.price * cart[i]['quantity'])

                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']

                item = {
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'imageURL': product.imageURL,
                    },
                    'quantity': cart[i]['quantity'],
                    'get_total': total,
                }
                items.append(item)

        context = {'items': items, 'order': order, 'cartItems': cartItems, 'shipping': False}
        return render(request, self.template_name, context)


class CheckoutView(View):
    template_name = 'store/checkout.html'
    context = {}

    def get(self, request):
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0}
            cartItems = order['get_cart_items']
        context = {'items': items, 'order': order, 'cartItems': cartItems, 'shipping': False}
        return render(request, self.template_name, context)

    def post(self, request):
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0}
            cartItems = order['get_cart_items']
        context = {'items': items, 'order': order, 'cartItems': cartItems, 'shipping': False}
        return render(request, self.template_name, context)


class UpdateItemView(View):
    def get(self, request):
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']
        print(action)
        print(productId)

        return JsonResponse('Item was added to cart', safe=False)

    def post(self, request):
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']
        print(action)
        print(productId)

        customer = request.user.customer
        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
        elif action == 'remove':
            orderItem.quantity = (orderItem.quantity - 1)

        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()

        return JsonResponse('Item was added to cart', safe=False)


class ProcessOrderView(View):
    def get(self, request):
        print('data', request.body)
        return JsonResponse('Payment complete!', safe=False)

    def post(self, request):
        transaction_id = datetime.datetime.now().timestamp()
        data = json.loads(request.body)

        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            total = float(data['form']['total'])
            order.transaction_id = transaction_id

            if total == order.get_cart_total:
                order.complete = True
            order.save()

            if order.shipping is True:
                ShippingAddress.objects.create(
                    customer=customer,
                    order=order,
                    address=data['shipping']['address'],
                    city=data['shipping']['city'],
                    state=data['shipping']['state'],
                    zipcode=data['shipping']['zipcode'],
                )

        else:
            print('User is not logged in')
        return JsonResponse('Payment complete!', safe=False)
