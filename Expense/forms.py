from django.forms import ModelForm
from django import forms

from Expense.models import Material, Purchase, PurchaseItem

# Create your forms here.

class MaterialForm(ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'price', 'category', 'quantity']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

class PurchaseForm(ModelForm):
    class Meta:
        model = Purchase
        fields = []
        

class PurchaseItemForm(ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ['material', 'discount']