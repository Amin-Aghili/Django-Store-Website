from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('', views.StoreView.as_view(), name='store'),
    # path('cart/', views.CartView.as_view(), name='cart'),
    # path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    # path('update_item/', views.UpdateItemView.as_view(), name='update_item'),
    # path('process_order/', views.ProcessOrderView.as_view(), name='process_order'),
]