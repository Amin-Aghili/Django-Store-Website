from django.shortcuts import render
from django.views import View
from .models import *


class StoreView(View):
    products = Product.objects.all()
    template_name = 'store/store.html'
    context = {'products': products}

    def get(self, request):
        return render(request, self.template_name, self.context)

    def post(self, request):
        return render(request, self.template_name, self.context)


class CartView(View):
    template_name = 'store/cart.html'

    def get(self, request):
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
        else:
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0}
        context = {'items': items, 'order': order}
        return render(request, self.template_name, context)

    def post(self, request):
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
        else:
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0}
        context = {'items': items, 'order': order}
        return render(request, self.template_name, context)


class CheckoutView(View):
    template_name = 'store/checkout.html'
    context = {}

    def get(self, request):
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
        else:
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0}
        context = {'items': items, 'order': order}
        return render(request, self.template_name, context)

    def post(self, request):
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
        else:
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0}
        context = {'items': items, 'order': order}
        return render(request, self.template_name, context)