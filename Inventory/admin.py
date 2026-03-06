from django.contrib import admin
from Inventory.models import Material, MaterialPreset, MaterialPresetItem

# Register your models here.

admin.site.register(Material)
admin.site.register(MaterialPreset)
admin.site.register(MaterialPresetItem)