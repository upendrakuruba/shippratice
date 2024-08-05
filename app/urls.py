from django.urls import path
from app import views
urlpatterns = [
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product-detail'),
    path('buy/<int:product_id>/', views.buy_now, name='buy-now'),
    path('orders/', views.orders, name='orders'),
    path('<slug:category_slug>/', views.mobile, name='mobile'),
]
