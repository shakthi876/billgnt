from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

# Create your models here.

class Items(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default='')
    Product_Id = models.IntegerField()
    Product_name = models.CharField(max_length=30)
    Price = models.FloatField()

    def __str__(self):
        return self.Product_name