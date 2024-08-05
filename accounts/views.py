from django.shortcuts import render,redirect,get_object_or_404
from .forms import *
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import HttpResponse
from .models import *
from carts.views import _cart_id
import requests 
# Create your views here.
@login_required(login_url='login')
def profile(request):
 if request.method == 'POST':
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            username = form.cleaned_data['username']
            address_line_1 = form.cleaned_data['address_line_1']
            address_line_2 = form.cleaned_data['address_line_2']
            zipcode = form.cleaned_data['zipcode']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            user = UserProfile(user=user,address_line_1=address_line_1,address_line_2=address_line_2,username=username,city=city,zipcode=zipcode,state=state)
            user.save()
            messages.success(request,' Your Profile Created .')
            return redirect('address')
 else:
    form = CustomerProfileForm
    context = {
        'form':form
    }
    return render(request, 'app/profile.html',context)




@login_required(login_url='login')
def address(request):
    userprofile = get_object_or_404(UserProfile,user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST,instance=request.user)
        profile_form = UserProfileForm(request.POST,request.FILES,instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Your profile has been updated')
            return redirect('address')
        else:
            print('10*__________',user_form)
            print('10*--------------',profile_form)
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form':user_form,
        'profile_form':profile_form,
        'userprofile':userprofile,
    }
    return render(request, 'app/address.html',context)


@login_required(login_url='login')
def change_password(request):
 if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)
    
        if new_password == confirm_password:
            success = user.check_password(current_password)
             
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request,'Password Updated Successfully.')
                return redirect('changepassword')
            else:
                messages.error(request,'Please Enter Valid Password')
                return redirect('changepassword')

        else:
            messages.error(request,'Password does not match')
            return redirect('changepassword')
 return render(request, 'app/changepassword.html')


def login(request):
 if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email,password=password)

        if user is not None:
           try:
               cart = Cart.objects.get(cart_id=_cart_id(request))
               is_cart_item_exists = Cartitem.objects.filter(cart=cart).exists()
               if is_cart_item_exists:
                   cart_item = Cartitem.objects.filter(cart=cart)
                   for item in cart_item:
                       item.user = user
                       item.save()
           except:
               pass
           auth.login(request,user)
           messages.success(request,'Your Now Logged in')
           url = request.META.get("HTTP_REFERER")
           try:
                query = requests.utils.urlparse(url).query
                # print('query ->',query)
                params = dict(x.split("=") for x in query.split("&"))
                if 'next' in params:
                    nextpage = params['next']
                    return redirect(nextpage)
                # print('10*__________',params)
    
           except:
                return redirect('store')
        else:
           messages.error(request,'Invalid Credentials')
 return render(request, 'app/login.html')

def customerregistration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_nunber = form.cleaned_data['phone_nunber']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = Account.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.phone_nunber = phone_nunber
            user.save()
            curren_site = get_current_site(request)
            email_subject = 'Please activate your account'
            message = render_to_string("account_verification_email.html",{
                'user':user,
                'domain':curren_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(email_subject,message,to=[to_email])
            send_email.send()
            # messages.success(request,'Thankyou for registerring with us. we have send you a verification email to your email address[kurumaupendra@gmail.com]. Please verify it.')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()
    context = {
    'form':form
    }
    return render(request, 'app/customerregistration.html',context)

def Logout_view(request):
   auth.logout(request)
   messages.success(request,'Your Now Logged Out')
   return redirect('login')


def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,'Congratulations Your Account is Activated')
        return redirect('login')
    else:
        messages.error(request,'Invalid activation link')
        return redirect('register')
    


def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            curren_site = get_current_site(request)
            email_subject = 'Reset Your Password'
            message = render_to_string("app/reset_password_email.html",{
                'user':user,
                'domain':curren_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(email_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'Password Reset email has been sent to your address .')
            return redirect('login')
        else:
            messages.error(request,'Account does not exit')
            return redirect('forgotpassword')
    return render(request,'app/forgotpassword.html')


def resetpassword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request,'Reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request,'This link has been expired')
        return redirect('login')
    

def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password Reset Successfull')
            return redirect('login')
        else:
            messages.error(request,'Password do not match')
            return redirect('resetpassword')
    else:
        return render(request,'app/resetpassword.html')
    
@login_required(login_url='login')
def checkout(request,total=0,quantity=0,cart_item=None):
    if request.user.is_authenticated:
        cart_items = Cartitem.objects.filter(user=request.user,is_active=True)
        address = UserProfile.objects.filter(user=request.user)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = Cartitem.objects.filter(cart=cart,is_active=True)
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax    
    context = {
        'cart_items':cart_items,
        'address':address,
        'total':total,
        'grand_total':grand_total

    }
    return render(request, 'app/checkout.html',context)


def direct_checkout(request,product_id):
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
            return redirect('checkout')
            
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
    return redirect('cart')

def error_404(request,exception):
    return render(request,'app/404_page.html')