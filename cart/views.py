from django.shortcuts import render
from django.views import View


class CartView(View):
    template_name = 'cart/cart.html'
    context = {}

    def post(self, request):
        return render(request, self.template_name, self.context)