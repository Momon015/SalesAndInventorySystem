from django.forms import ModelForm
from django import forms

from Inventory.models import Material

# Create your forms here.

class MaterialForm(ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'price', 'category', 'quantity']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)