from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CompanyDetails(models.Model):
    
    Code = models.CharField(unique =True,max_length=30)
    Company_name = models.CharField(max_length=30)
    Owner_Email_Address = models.CharField(max_length=50)
    AdminPass = models.CharField(max_length=50)
    

    def __str__(self):
        return self.Company_name

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username