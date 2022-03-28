from django.shortcuts import render
from django.views import View
from core.utils import cart_data
from products.models import Product


class StoreView(View):
    products = Product.objects.all()
    template_name = 'store/store.html'

    def get(self, request):
        try:
            data = cart_data(request)
            cart_items = data['cart_items']
            context = {'cart_items': cart_items, 'shipping': False}

        except:
            context = {'cart_items': 0, 'shipping': False}

        return render(request, self.template_name, context)

    def post(self, request):
        data = cart_data(request)
        cart_items = data['cart_items']

        context = {'products': self.products, 'cart_items': cart_items, 'shipping': False}
        return render(request, self.template_name, context)
