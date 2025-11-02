from django.db import models
from django.utils.text import slugify

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class SlugModel(models.Model):
    slug = models.SlugField(null=True, blank=True, unique=True)
    
    class Meta:
        abstract = True
    

class Category(SlugModel):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'Product_category'

class StatusModel(SlugModel, TimeStampModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('paid', 'Paid'),
        ('canceled', 'Canceled'),
    ]
    
    name = models.CharField(max_length=50, choices=STATUS_CHOICES, unique=True)
    
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
