from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

from api.config.base import BaseModel
from api.helpers.permission import SYSTEM_PERMISSIONS, SYSTEM_ROLES




class Roles(BaseModel):
    name = models.CharField(max_length=150, choices=SYSTEM_ROLES, unique=True)
    description = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.description or self.name

class Permission(BaseModel):
    name = models.CharField(max_length=150, unique=True, choices=SYSTEM_PERMISSIONS)
    description = models.CharField(max_length=200, null=True, blank=True)
        
    def __str__(self):
        return self.name


class RolePermission(BaseModel):
    role = models.OneToOneField(Roles, on_delete=models.CASCADE, unique=True, related_name="role_permissions")
    permissions = models.ManyToManyField(Permission, blank=True, verbose_name="Permissions", related_name="permission_roles")
    
    def __str__(self):
        return f"{self.role.name}"
    

class UserRole(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_roles")
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, related_name="role_users")
    
    # add extra permissions for the user in addition to their role permissions
    permissions = models.ManyToManyField(Permission, blank=True, verbose_name="Extra Permissions", related_name="user_permissions")
    
    def __str__(self):
        return f"{self.user.username} - {self.role.name}"
    
    
    
    def transform_extra_permissions(self):
        return list(
            self.permissions.values("id", "name")
        )

    def transform_role_permissions(self):
        try:
            return list(
                self.role.role_permissions.permissions.values(
                    "id",
                    "name"
                )
            )
        except RolePermission.DoesNotExist:
            return []

    def transform_permissions(self):
        permissions = {
            "permissions": [],
            "extra_permissions": []
        }

        # Role permissions
        for perm in self.transform_role_permissions():
            permissions["permissions"].append(perm)

        # Extra permissions
        for perm in self.transform_extra_permissions():
            permissions["extra_permissions"].append(perm)

        return permissions
        

        
    
    def check_permissions(self):
        permissions = {}

        # Role permissions
        for perm in self.transform_role_permissions():
            permissions[perm["id"]] = perm

        # Extra permissions
        for perm in self.transform_extra_permissions():
            permissions[perm["id"]] = perm

        return list(permissions.values())