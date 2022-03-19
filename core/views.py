from django.shortcuts import render
from django.views import View
from .forms import TrendyolUrlForm
from .price_trendyol import TrendyolShop
from .utils import cart_data


class HomeView(View):
    url_form = TrendyolUrlForm()
    template_name = 'core/home.html'
    trendyol = TrendyolShop()
    form_class_url = TrendyolUrlForm
    exchange_rates = trendyol.exchange_rates()

    def get(self, request):

        data = cart_data(request)
        cart_items = data['cart_items']
        exchange_rates = self.trendyol.exchange_rates()
        form_url = self.form_class_url()
        context = {
            'form_url': form_url,
            'exchange_rates': exchange_rates,
            'cart_items': cart_items,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        data = cart_data(request)
        cart_items = data['cart_items']
        form_url = self.form_class_url(request.POST)
        selected_size = request.POST.get('size')
        if selected_size:
            form_url = self.form_class_url()
            sizes = self.trendyol.is_sizes()
            image_url = self.trendyol.images_url()
            price, price_tl = self.trendyol.selected_size(selected_size, request, self.exchange_rates)
            return render(
                request,
                self.template_name,
                {
                    'form_url': form_url,
                    'sizes': sizes,
                    'exchange_rates': self.exchange_rates,
                    'price': price,
                    'image_url': image_url,
                    'selected_size': selected_size,
                    'price_tl': price_tl,
                    'cart_items': cart_items,
                }
            )
        else:
            if form_url.is_valid():
                url = form_url.cleaned_data['url']
                if self.trendyol.check_trendyol_url(request, url):
                    price, price_tl = self.trendyol.price(request, self.exchange_rates)
                    if price:
                        image_url = self.trendyol.images_url()
                        if self.trendyol.is_sizes():
                            sizes = self.trendyol.is_sizes()
                            return render(
                                request,
                                self.template_name,
                                {
                                    'form_url': form_url,
                                    'sizes': sizes,
                                    'exchange_rates': self.exchange_rates,
                                    'price': price,
                                    'image_url': image_url,
                                    'price_tl': price_tl,
                                    'cart_items': cart_items,
                                }
                            )
                        else:
                            return render(
                                request,
                                self.template_name,
                                {
                                    'form_url': form_url,
                                    'exchange_rates': self.exchange_rates,
                                    'price': price,
                                    'image_url': image_url,
                                    'price_tl': price_tl,
                                    'cart_items': cart_items,
                                }
                            )
            return render(request, self.template_name, {'form_url': form_url})
