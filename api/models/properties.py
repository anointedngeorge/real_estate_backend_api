from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

from api.config.base import BaseModel
from api.schema.usersSchema import PropertiesPlotsSchema


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
    name = models.CharField(max_length=150, unique=True)
    image = models.CharField(max_length=250, null=True, blank=True)
    slug = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    status = models.CharField(max_length=150,  choices=StatusType)
    property_types = models.CharField(max_length=150,  choices=PropertyTypes )
    description = models.TextField(null=True, blank=True)
    actual_price = models.DecimalField(max_digits=20, decimal_places=2)
    selling_price = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    features = models.JSONField(default=dict)
    has_plots = models.BooleanField(default=False)
    
    # 
    def __str__(self):
        return self.name
    
    @property
    def plots(self):
        qs = self.properties_plots.filter(status=False)
        rp = [PropertiesPlotsSchema.validate(x).model_dump() for x in qs]
        return rp
    


class PropertyPlots(BaseModel):
    properties = models.ForeignKey("api.Properties", on_delete=models.CASCADE, related_name="properties_plots")
    plot_number = models.CharField(max_length=150, unique=True)
    plot_price = models.DecimalField(max_digits=20, decimal_places=2)
    uid = models.CharField(max_length=250, unique=True)
    status = models.BooleanField(default=False )
    
    
