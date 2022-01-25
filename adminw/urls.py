from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('display/',views.display,name='display'),
    path('delete/<int:pk>/',views.deleteitem,name='deleteitem'),
    path('modify/<int:pk>/',views.modify,name='modify'),
    path('deleteall/',views.deleteall,name='deleteall'),
]