from django.db import models

from Product.models import Product

from user.models import User

from django.db.models import Sum, Avg

from Expense.models import Employee

from decimal import Decimal

from core.models import TimeStampModel
from django.core.exceptions import ValidationError

# Create your models here.

class SaleQuerySet(models.QuerySet):
    def total_sold(self):
        return self.aggregate(total_sold=Sum('total_cost'))['total_sold']

    def average_total_sold(self):
        return self.aggregate(average_total_sold=Avg('total_cost'))['average_total_sold']
    

class Sale(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales', null=True, blank=True)
    date = models.DateField(auto_now_add=True, db_index=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    line_count = models.PositiveIntegerField(default=0)
    
    objects = SaleQuerySet.as_manager()
    
    def __str__(self):
        return f"Date: {self.date} - {self.total_cost}"
    
    def quantity_item(self):
        return sum(item.quantity for item in self.sale_items.all())
        
class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='sale_items', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sale_items', null=True, blank=True)
    price_at_sale = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)
    quantity = models.PositiveIntegerField(default=1)
    unsold_quantity = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    def save(self, *args, **kwargs):
        if not self.price_at_sale:
            self.price_at_sale = self.product.selling_price
        return super().save(*args, **kwargs)
        
    def clean(self):
        if self.prepared_quantity > self.quantity:
            raise ValidationError('Quantity should not exceed to prepared quantity.')
    
    @property
    def unsold_product_cost(self):
        return self.cost_price * self.unsold_quantity
    
    @property
    def total_sold_per_item(self):
        return self.price_at_sale * self.quantity
    
class SaleEmployee(TimeStampModel):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='sale_employees', null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='sale_employees', null=True, blank=True)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Sale Record ID: #{self.sale.id} - {self.employee.name}"
        
