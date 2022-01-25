from django.contrib import admin

from accounts.models import CompanyDetails, Profile


#from accounts.views import login

# Register your models here.

admin.site.register(CompanyDetails)

admin.site.register(Profile)