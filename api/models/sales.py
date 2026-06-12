from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from api.config.base import BaseModel


class PaymentPlan(models.TextChoices):
    '6', "6-Months"
    '3', '3-Months'
    '12', '12-Months'
    'outright', 'Outright'
    
    
class Status(models.TextChoices):
    'in_progress', "In Progress"
    'failed', 'Failed'
    'completed', 'completed'
    'cancelled', 'Cancelled'
    'reversed', 'Reversed'




class Sales(BaseModel):
    properties = models.ForeignKey("api.Properties", on_delete=models.SET_NULL, null=True, blank=True, related_name="sale_property")
    client = models.ForeignKey("api.EstateClients", on_delete=models.SET_NULL, null=True, blank=True, related_name="sales_client")
    realtor = models.ForeignKey("api.Realtors", on_delete=models.SET_NULL, null=True, blank=True, related_name="sales_realtor")

    payment_plan = models.CharField(max_length=150, choices=PaymentPlan)
    status = models.CharField(max_length=150, choices=Status)
    
    plots = models.CharField(max_length=150, default=None, blank=True, null=True)
    
    
    sales_date = models.DateField(auto_now_add=True)
    sales_date_time = models.TimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    # 
    def __str__(self):
        return super().__str__()
    
    def get_name(self):
        return f"{self.id} - {self.properties.name} "
    
    @property
    def commission(self):
        return  {'direct': '9000', 'upline': '78999'}
    




class DateTracker(BaseModel):
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()

    class Meta:
        unique_together = ("year", "month")