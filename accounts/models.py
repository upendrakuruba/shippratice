from django.db import models
from app.models import *
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(Account,on_delete=models.CASCADE)
    username = models.CharField(blank=True,max_length=100)
    address_line_1 = models.CharField(blank=True,max_length=100)
    address_line_2 = models.CharField(blank=True,max_length=100)
    mobile = models.CharField( max_length=50,blank=True)
    zipcode = models.CharField(max_length=20,blank=True)
    city = models.CharField(blank=True,max_length=20)
    state = models.CharField(blank=True,max_length=20)
    profile_picture = models.ImageField( upload_to='userprofile')

    def __str__(self):
        return self.user.first_name
    
    def full_address(self):
        return f"{self.address_line_1} {self.address_line_2} "
    
