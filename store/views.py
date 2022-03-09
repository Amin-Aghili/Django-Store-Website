from django.shortcuts import render
from django.views import View
from .forms import TrendyolUrlForm


class StoreView(View):
    url_form = TrendyolUrlForm()
    template_name = 'store/store.html'
    context = {'url_form': url_form}

    def get(self, request):
        return render(request, self.template_name, self.context)

    def post(self, request):
        return render(request, self.template_name, self.context)


class CartView(View):
    template_name = 'store/cart.html'
    context = {}

    def get(self, request):
        return render(request, self.template_name, self.context)

    def post(self, request):
        return render(request, self.template_name, self.context)


class CheckoutView(View):
    template_name = 'store/checkout.html'
    context = {}

    def get(self, request):
        return render(request, self.template_name, self.context)

    def post(self, request):
        return render(request, self.template_name, self.context)