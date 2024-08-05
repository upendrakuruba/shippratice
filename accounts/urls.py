from django.urls import path
from .views import *
urlpatterns = [
    path('profile/', profile, name='profile'),
    path('', profile, name='profile'),
    path('address/', address, name='address'),
    path('changepassword/', change_password, name='changepassword'),
    path('login/', login, name='login'),
    path('Logout_view/', Logout_view, name='Logout_view'),
    path('registration/', customerregistration, name='registration'),
    path("activate/<uidb64>/<token>/", activate, name="activate"),
    path("forgotpassword/", forgotpassword, name="forgotpassword"),
    path("resetpassword_validate/<uidb64>/<token>/", resetpassword_validate, name="resetpassword_validate"),
    path("resetpassword/", resetpassword, name="resetpassword"),
    path('checkout/', checkout, name='checkout'),
    path('direct_checkout/<int:product_id>/', direct_checkout, name='direct_checkout'),
    path('error_404', error_404,name='error_404'),

]
