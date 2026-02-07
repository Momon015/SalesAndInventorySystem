from django.db import models
from django.utils.text import slugify

from core.models import TimeStampModel, SlugModel, Category, StatusModel
from Inventory.models import Material

from django.utils import timezone

from django.db.models import Sum, Avg, Value

from django.db.models.functions import Coalesce
from decimal import Decimal

from user.models import User

# Create your models here.

"""
This is a custom queryset for computing the average
and the sum of the total cost make sure u save it to 
the parent model use either objects(recommended) or 
any other name so u can simply called Purchase.objects.
<function_name>().
"""

class PurchaseQuerySet(models.QuerySet):
    def purchase_total_cost(self):
        return self.aggregate(monthly_cost=Coalesce(Sum('total_cost'), Value(Decimal('0'))))['monthly_cost']
        
    def average_total_cost(self):
        return self.aggregate(monthly_average_cost=Coalesce(Avg('total_cost'), Value(Decimal('0'))))['monthly_average_cost']
    

    
class Purchase(TimeStampModel):
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.ForeignKey(StatusModel, on_delete=models.SET_NULL, null=True)
    is_paid = models.BooleanField(default=False)
    line_count = models.PositiveIntegerField(default=0)
    purchase_date = models.DateField(auto_now_add=True, null=True, db_index=True) # remove NULL when you reset the DB
    
    # save the custom queryset as_manager()
    objects = PurchaseQuerySet.as_manager()
    
    def __str__(self):
        return f"Purchase ID: #{self.id} - {self.formatted_date}, Total Cost: {self.total_cost}"
    
    def save(self, *args, **kwargs):
        if self.status and self.status.slug == 'paid':
            self.is_paid = True
            
        # if not self.slug and self.status:
        #     self.slug = self.status.slug
            
        # always update the total cost
        # if self.pk:
        #     self.total_cost = self.total_cost_per_purchase
        super().save(*args, **kwargs)
        
    @property
    def formatted_date(self):
        local_time = timezone.localtime(self.created_at)
        return local_time.strftime("%B %d %Y %I:%M %p")
    
    @property
    def total_cost_per_purchase(self):
        return sum(item.total_price_per_item for item in self.materials.all())
    
    @property
    def total_quantity_items(self):
        return sum(item.quantity for item in self.materials.all())
    
    # ADMIN PANEL
    
    @property
    def total_discount(self):
        return sum(item.discount if item.discount > 0 else 0 for item in self.materials.all())

    @property
    def purchase_items(self):
        return [item.material.name for item in self.materials.all()]
    
    @property
    def quantity_items(self):
        return [item.quantity for item in self.materials.all()]



        
class PurchaseItem(TimeStampModel):
    purchase = models.ForeignKey(Purchase, on_delete=models.SET_NULL, related_name='materials', null=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='items')
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.material.name} - ({self.material.price} x {self.quantity}) - {self.discount} = {self.total_item_discount}"

    @property
    def material_price(self):
        return self.material.price
    
    @property
    def total_price_per_item(self):
        return self.material.price * self.quantity
    
    @property
    def total_item_discount(self):
        return self.total_price_per_item - self.discount
    

  
    # def material_discount(self):
    #     if self.discount:
    #         return self.total_price_per_item - self.discount
    #     return self.total_price_per_item


class Preset(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='presets')
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    

    def __str__(self):
        return self.name


class PresetItem(models.Model):
    class Meta:
        unique_together = ('preset', 'material')
        ordering = ['id']
        
    preset = models.ForeignKey(Preset, on_delete=models.CASCADE, related_name='preset_items')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='preset_items')
    quantity = models.PositiveIntegerField(default=1)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.material} x {self.quantity} - Discount: {self.discount}"
    
    @property
    def total_line_cost(self):
        return self.material.price * self.quantity