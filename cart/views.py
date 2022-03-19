from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from core.utils import cart_data
import json
from products.models import Product
from order.models import Order, OrderItem


class CartView(View):
    template_name = 'cart/cart.html'

    def get(self, request):
        data = cart_data(request)
        cart_items = data['cart_items']
        order = data['order']
        items = data['items']

        context = {'items': items, 'order': order, 'cart_items': cart_items, 'shipping': False}
        return render(request, self.template_name, context)

    def post(self, request):
        data = cart_data(request)
        cart_items = data['cart_items']
        order = data['order']
        items = data['items']

        context = {'items': items, 'order': order, 'cart_items': cart_items, 'shipping': False}
        return render(request, self.template_name, context)


class UpdateItemView(View):
    def get(self, request):
        data = json.loads(request.body)
        product_id = data['product_id']
        action = data['action']
        print(action)
        print(product_id)

        return JsonResponse('Item was added to cart', safe=False)

    def post(self, request):
        data = json.loads(request.body)
        product_id = data['product_id']
        action = data['action']
        print(action)
        print(product_id)

        customer = request.user.customer  # get the customer???????
        product = Product.objects.get(id=product_id)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            order_item.quantity = (order_item.quantity + 1)
        elif action == 'remove':
            order_item.quantity = (order_item.quantity - 1)

        order_item.save()

        if order_item.quantity <= 0:
            order_item.delete()

        return JsonResponse('Item was added to cart', safe=False)
