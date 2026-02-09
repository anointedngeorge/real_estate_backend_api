import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

from api.config.base import BaseModel





class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    has_agreed_terms = models.BooleanField(default=False)
    
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    
    role = models.CharField(max_length=50, choices=[
        ('admin', 'Admin'),
        ('agent', 'Agent'),
        ('buyer', 'Buyer'), 
    ], default='buyer')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    

    def __str__(self):
        return self.email
    
    
    


class UserKyc(BaseModel):
    picture = models.CharField(max_length=255, null=True, blank=True)
    
    
    


class BlackListedTokens(BaseModel):
    jti = models.CharField(max_length=255, unique=True)
    token = models.TextField()
    