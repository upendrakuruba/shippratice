from django.urls import path
from .views import *
urlpatterns = [
    path('', store,name='store'),
]
