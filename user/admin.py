from django.contrib import admin

from user.models import User, EmailOTP

# Register your models here.

admin.site.register(User)
admin.site.register(EmailOTP)