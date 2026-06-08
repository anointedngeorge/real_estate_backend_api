from typing import Dict, List
import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

from api.config.base import BaseModel
from api.helpers.permission import SYSTEM_ROLES, get_role_permissions
from api.models.authorization import RolePermission, UserRole
from django.shortcuts import get_object_or_404



class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    has_agreed_terms = models.BooleanField(default=False)

    phone_number = models.CharField(max_length=20, null=True, blank=True)

    role = models.CharField(
        max_length=50,
        choices=SYSTEM_ROLES,
        default="buyer",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "role"]

    def __str__(self):
        return self.first_name + " " + self.last_name

    def get_fullname(self):
        return self.first_name + " " + self.last_name
    
    
    @property
    def permissions(self):
        try:
            user_role = self.user_roles.select_related(
                "role"
            ).prefetch_related(
                "permissions",
                "role__role_permissions__permissions"
            ).get()

            iroles = user_role.transform_permissions()
            return iroles

        except UserRole.DoesNotExist:
            return {"permissions": [], "extra_permissions": []  }
    

    
    @property
    def login_histories(self):
        hist = self.user_login_tracker.all()
        return [
            {   
                "id": x.id,
                "user": x.user.get_fullname(),
                "agent": x.agent,
                "location": x.location,
                "platform": x.platform,
                "l_date": x.created_at,
            }
            for x in hist
        ]




class UserKyc(BaseModel):
    picture = models.CharField(max_length=255, null=True, blank=True)


class LoginTracker(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_login_tracker",
    )
    agent = models.TextField()
    location = models.CharField(max_length=255, null=True, blank=True)
    platform = models.CharField(max_length=255, null=True, blank=True)


class BlackListedTokens(BaseModel):
    jti = models.CharField(max_length=255, null=True, blank=True)
    token = models.TextField()
