from django.urls import path
from .views import *

app_name = 'frontend'

urlpatterns = [
    path('cart/', CartView.as_view(),name = 'cart' ),
    path('addresses/',AddressListView.as_view(),name = 'address-list'),
    path('checkout/',PaymentView.as_view(),name = 'checkout'),
    # path('orders',OrderView.as_view()),
    # path('address',AddressView.as_view),

]