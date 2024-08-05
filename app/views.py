from django.shortcuts import render,get_object_or_404,redirect
from category.models import *
from store.models import *
from .models import *
from carts.views import _cart_id
from django.contrib.auth.decorators import login_required



def product_detail(request,category_slug,product_slug):
 try:
  single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
  in_cart = Cartitem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()

 except Exception as e:
    raise e
 context = {
  'single_product':single_product,
  'in_cart':in_cart
 }
 return render(request, 'app/productdetail.html',context)



@login_required(login_url='login')
def buy_now(request,product_id):
 current_user = request.user
 product = Product.objects.get(id=product_id)
 if current_user.is_authenticated:
  try:
   cart_item = Cartitem.objects.get(product=product,user=current_user)
   cart_item.quantity += 1
   cart_item.save()
  except Cartitem.DoesNotExist:
   cart_item = Cartitem.objects.create(
   product=product,
   quantity = 1,
   user=current_user,
  )
  cart_item.save()
  return redirect('cart')
 
 else:
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
        cart_id = _cart_id(request)
        )
        cart.save()
    try:
        cart_item = Cartitem.objects.get(product=product,cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except Cartitem.DoesNotExist:
        cart_item = Cartitem.objects.create(
        product=product,
        quantity = 1,
        cart=cart,
        )
        cart_item.save()
    return redirect('checkout')



@login_required(login_url='login')
def orders(request):
 return render(request, 'app/orders.html')


def mobile(request,category_slug=None):
 categories = None
 products = None
 if category_slug !=None:
  categories = get_object_or_404(Category,slug=category_slug)
  products = Product.objects.filter(category=categories, is_available=True)
  prod = Product.objects.all().filter(is_available=True)


  context = {
   'products':products,
   'categories':categories,
  }
 return render(request, 'app/mobile.html',context)


