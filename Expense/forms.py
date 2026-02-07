from django.forms import ModelForm
from django import forms

from Expense.models import Purchase, PurchaseItem, Preset, PresetItem

# Create your forms here.

class PurchaseForm(ModelForm):
    class Meta:
        model = Purchase
        fields = []
        

class PurchaseItemForm(ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ['material', 'discount']

class PurchaseFilterForm(forms.Form):
    search = forms.CharField(required=False)
    select_month = forms.CharField(required=False)
    period = forms.CharField(required=False)
    
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
class PresetForm(ModelForm):
    class Meta:
        model = Preset
        fields = ['name']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['name'].required = False


class PresetItemForm(ModelForm):
    class Meta:
        model = PresetItem
        fields = ['material', 'quantity']
        


