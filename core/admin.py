from django.contrib import admin

from core.models import StatusModel, Category

# Register your models here.

admin.site.register(StatusModel)
admin.site.register(Category)