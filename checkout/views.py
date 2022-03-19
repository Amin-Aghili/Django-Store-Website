from django.shortcuts import render
from django.views import View
from core.utils import cart_data


class CheckoutView(View):
    template_name = 'checkout/checkout.html'
    context = {}

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
