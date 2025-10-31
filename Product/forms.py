from django.forms import ModelForm
from django import forms

from Product.models import Product

# Create your forms here.

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category']
        
        
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        