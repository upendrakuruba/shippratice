from typing import Any
from django import forms
from app.models import Account
from .models import *
from django.contrib.auth.forms import PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.utils.translation import gettext,gettext_lazy as _
from django.contrib.auth import password_validation


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password',
        'class':'form-contrl',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm Password'
    }))
    class Meta:
        model = Account
        fields = ['first_name','last_name','phone_nunber','email','password']


    def __init__(self,*args, **kwargs):
        super(RegistrationForm,self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['phone_nunber'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter First Name'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Password Does Not Match!')
        



class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username','address_line_1','address_line_2','zipcode','city','state']

    def __init__(self,*args, **kwargs):
        super(CustomerProfileForm,self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Enter Username'
        self.fields['address_line_1'].widget.attrs['placeholder'] = 'Enter address_line_1'
        self.fields['address_line_2'].widget.attrs['placeholder'] = 'Enter address_line_2'
        self.fields['city'].widget.attrs['placeholder'] = 'Enter city'
        self.fields['state'].widget.attrs['placeholder'] = 'Enter state'
        self.fields['zipcode'].widget.attrs['placeholder'] = 'Enter zipcode'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'




class UserForm(forms.ModelForm):
    class Meta:
     model = Account
     fields = ('first_name','last_name','phone_nunber','email')
    def __init__(self,*args, **kwargs):
        super(UserForm,self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    class Meta:

        model = UserProfile
        fields = ('username','address_line_1','address_line_2','city','state','zipcode')
    def __init__(self,*args, **kwargs):
        super(UserProfileForm,self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'




