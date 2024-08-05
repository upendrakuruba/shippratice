from django.shortcuts import render
from store.models import *
def store(request):
 products = Product.objects.all().filter(is_available=True)
 context = {
  'products':products,

 }
 return render(request, 'app/mobile.html',context)
