from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
import json
import datetime
from core.utils import guest_order
from .models import Order
from .models import ShippingAddress


class ProcessOrderView(View):
    def get(self, request):
        print('data', request.body)
        return JsonResponse('Payment complete!', safe=False)

    def post(self, request):
        transaction_id = datetime.datetime.now().timestamp()
        data = json.loads(request.body)

        if request.user.is_authenticated:
            customer = request.user
            order, created = Order.objects.get_or_create(customer=customer, complete=False)

        else:
            customer, order = guest_order(request, data)

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

        return JsonResponse('Payment complete!', safe=False)
