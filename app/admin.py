from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.utils.html import format_html
# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email','first_name','last_name','username','last_login','is_active','date_join')
    list_display_links = ('email','first_name','last_name')
    readonly_fields = ('last_login','date_join')
    ordering = ('-date_join',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id','date_added')


class CartitemAdmin(admin.ModelAdmin):
    list_display = ('product','cart','quantity','is_active')

admin.site.register(Cart,CartAdmin)
admin.site.register(Cartitem,CartitemAdmin)
admin.site.register(Account,AccountAdmin)