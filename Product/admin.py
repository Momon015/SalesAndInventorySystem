from django.contrib import admin

from Product.models import Product, ProductPreset, ProductPresetItem

# Register your models here.

admin.site.register(Product)
admin.site.register(ProductPreset)
admin.site.register(ProductPresetItem)