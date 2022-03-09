from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('', views.StoreView.as_view(), name='store'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
]