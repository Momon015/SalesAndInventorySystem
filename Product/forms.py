from django.forms import ModelForm
from django import forms

from Product.models import Product

from core.models import Category

# Create your forms here.
        
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'cost_price', 'stock', 'selling_price', 'category']
    

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        def category_label(obj):
            return obj.name.title()
        

        self.fields['category'].queryset = Category.objects.filter(category_type='product')
        self.fields['category'].empty_label = None
        self.fields['category'].label_from_instance = category_label # or lambda obj: obj.name.title()
        
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class ProductFilterForm(forms.Form):
    search = forms.CharField(required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.none(), required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(category_type='product')
       

        
        