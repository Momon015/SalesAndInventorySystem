from django.db import models
from django.utils.text import slugify
from core.models import Category, SlugModel, TimeStampModel

# Create your models here.

class Product(SlugModel, TimeStampModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.cost_price:
            self.cost_price = 0
        super().save(*args, **kwargs)