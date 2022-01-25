from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Sales(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default='')
   
    Product_name = models.CharField(max_length=30)
    Price = models.FloatField()
    Quantity = models.FloatField()
    Total = models.FloatField()

    def __str__(self):
        return self.Product_name



class Bill(models.Model):
    BillNumber = models.IntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE,default='')

    def __str__(self):
        return str(self.BillNumber)
    
class SalesDetails(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default='')
    Did = models.IntegerField()
    BillNo = models.IntegerField()
    Sold_Date = models.DateField(null=True,blank=True)
    Item_name = models.CharField(max_length=30,null=True,blank=True)
    Quantity = models.FloatField(null=True,blank=True)
   

    def __str__(self):
        return self.Item_name



    