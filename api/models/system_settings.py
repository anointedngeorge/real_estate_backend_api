from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

from api.config.base import BaseModel




class SystemSettings(BaseModel):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=200)
    
    
    
    def __str__(self):
        return super().__str__()