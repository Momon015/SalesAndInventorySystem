from django.contrib import admin
from Expense.models import Material, PurchaseItem, Purchase

# Register your models here.
admin.site.register(Material)
admin.site.register(PurchaseItem)
admin.site.register(Purchase)
