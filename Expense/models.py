from django.db import models
from django.utils.text import slugify

from core.models import TimeStampModel, SlugModel, Category, StatusModel
from Inventory.models import Material

from django.utils import timezone

# Create your models here.
    
class Purchase(TimeStampModel):
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.ForeignKey(StatusModel, on_delete=models.SET_NULL, null=True)
    is_paid = models.BooleanField(default=False)
    
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
        return sum(item.material_discount() for item in self.materials.all())
    
    
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
        return f"Purchase ID: #{self.purchase.id}"
        # total = self.purchase.total_cost if self.purchase and self.purchase.total_cost else 0
        # return f"Purchase ID: #{self.purchase.id} - {self.total_price_per_item} - {self.discount} = {self.total_item_discount}"
    
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
