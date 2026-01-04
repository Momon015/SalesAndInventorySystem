from django.db import models

from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser

from core.models import SlugModel
from datetime import date, timedelta

from django.utils import timezone

from django.core.validators import RegexValidator

# Create your models here.

phone_validators = RegexValidator(
    regex=r'^0\d{10}$',
    message="Phone Number must be 11 digits."
)

password_validators = RegexValidator(
    regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[*!#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,}$',
    message='One Lowercase, One Uppercase and One Special symbol minimum'
)

ROLE_CHOICES = [
        ('developer', 'Developer'),
        ('owner', 'Owner'),
        ('staff', 'Staff'),
        
    ]

class User(AbstractUser, SlugModel):

    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True, validators=[phone_validators])
    locked_until = models.DateTimeField(null=True, blank=True)
    failed_attempts = models.PositiveIntegerField(default=0)
    password_changed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def is_locked(self):
        if self.locked_until:
            return timezone.now() < self.locked_until
        return False

  
    def register_failed_login(self):
        if self.is_locked():
            return
        else:
            self.failed_attempts += 1
            if self.failed_attempts > 4 and self.failed_attempts <= 5:
                self.locked_until = timezone.now() + timedelta(minutes=10)
                
    def reset_attempts(self):
        self.failed_attempts = 0
        self.locked_until = None
            

    @property
    def age(self):
        if not self.birthday:
            return None
        
        today = date.today()
        age = today.year - self.birthday.year
        if (today.month, today.day) < (self.birthday.month, self.birthday.day):
            age -= 1
        return age
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        
        if not self.name:
            self.name = self.first_name
        
        super().save(*args, **kwargs)
        

