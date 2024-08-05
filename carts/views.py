from django.shortcuts import render,redirect,get_object_or_404
from store.models import *
from carts.models import *
from app.models import *
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
def _cart_id(request):
 cart = request.session.session_key
 if not cart:
  cart = request.session.create()
 return cart




def add_to_cart(request,product_id):
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
    return redirect('cart')


def remove_cart(request,product_id):
 product = get_object_or_404(Product,id=product_id)
 if request.user.is_authenticated:
    cart_item = Cartitem.objects.get(product=product,user=request.user)
 else:
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = Cartitem.objects.get(product=product,cart=cart)
 if cart_item.quantity >1:
  cart_item.quantity -= 1
  cart_item.save()
 else:
  cart_item.delete()
 return redirect('cart')

def remove_cart_item(request,product_id):
 product = get_object_or_404(Product,id=product_id)
 if request.user.is_authenticated:
    cart_item = Cartitem.objects.get(product=product,user=request.user)
 else:
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = Cartitem.objects.get(product=product,cart=cart)
 cart_item.delete()
 return redirect('cart')




def cart(request,total=0,quantity=0,cart_item=None):
 
 try:
  cart_items = 0
  tax = 0
  grand_total = 0
  if request.user.is_authenticated:
   cart_items = Cartitem.objects.filter(user=request.user,is_active=True)
  else:
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_items = Cartitem.objects.filter(cart=cart,is_active=True)
  for cart_item in cart_items:
   total += (cart_item.product.price * cart_item.quantity)
   quantity += cart_item.quantity
   tax = (2 * total)/100
   grand_total = total + tax
 except ObjectDoesNotExist:
  pass
 context = {
  'total':total,
  'quantity':quantity,
  'cart_items':cart_items,
  'tax':tax,
  'grand_total':grand_total

 }
 return render(request, 'app/addtocart.html',context)
