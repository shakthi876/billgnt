from django.contrib import admin

from cashier.models import Bill, Sales, SalesDetails

# Register your models here.
admin.site.register(Sales)
admin.site.register(SalesDetails)
admin.site.register(Bill)