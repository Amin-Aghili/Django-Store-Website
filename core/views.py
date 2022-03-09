from django.shortcuts import render
from django.views import View
from .forms import TrendyolUrlForm


class HomeView(View):
    url_form = TrendyolUrlForm()
    template_name = 'core/home.html'
    context = {'url_form': url_form}

    def get(self, request):
        return render(request, self.template_name, self.context)

    def post(self, request):
        return render(request, self.template_name, self.context)