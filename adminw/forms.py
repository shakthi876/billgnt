from tkinter import Widget
from tkinter.ttk import Style
from typing import ItemsView
from django import forms

from adminw.models import Items

class ItemModifyForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = ['Product_Id', 'Product_name','Price']

      