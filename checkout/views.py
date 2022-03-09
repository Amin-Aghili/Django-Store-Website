from django.shortcuts import render
from django.views import View


class CheckoutView(View):
    template_name = 'checkout/checkout.html'
    context = {}

    def post(self, request):
        return render(request, self.template_name, self.context)

