from django.contrib import admin
from .models import *
from django.utils.html import format_html
# Register your models here.



class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self,object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
    thumbnail.short_description = 'Profile Picuture'
    list_display = ('user','city','state')

admin.site.register(UserProfile,UserProfileAdmin)
