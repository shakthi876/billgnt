from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('search/',views.search,name='search'),
    path('remove/<int:pk>/',views.remove,name='remove'),
    #path('removeall/',views.removeall,name='removeall'),
    #path('check/',views.check,name='check'),
    path('export/', views.export, name='export'),
    
]