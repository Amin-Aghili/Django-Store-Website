from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
import json
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
        context = {'items': items, 'order': order, 'cartItems': cartItems ,'shipping': False}
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