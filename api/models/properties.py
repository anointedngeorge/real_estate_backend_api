from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

from api.config.base import BaseModel


class StatusType(models.TextChoices):
    'available', "Available"
    'sold', 'Sold'
    'reserved', 'Reserved'



class PropertyTypes(models.TextChoices):
    'land', "Land"
    'house', 'House'
    'apartment', 'Apartment'
    'commercial', 'Commercial'
    


class Properties(BaseModel):
    name = models.CharField(max_length=150)
    image = models.CharField(max_length=250, null=True, blank=True)
    slug = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    status = models.CharField(max_length=150,  choices=StatusType)
    property_types = models.CharField(max_length=150,  choices=PropertyTypes )
    description = models.TextField(null=True, blank=True)
    actual_price = models.DecimalField(max_digits=20, decimal_places=2)
    selling_price = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    features = models.JSONField(default=dict)
    
    has_plots = models.BooleanField(default=False )
    
    # 
    def __str__(self):
        return super().__str__()
    


class PropertyPlots(BaseModel):
    pass