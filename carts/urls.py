from django.urls import path
from .views import *
urlpatterns = [
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add-to-cart'),
    path('cart/', cart, name='cart'),
    path('remove_cart/<int:product_id>/', remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/', remove_cart_item, name='remove_cart_item'),
]
