from django.contrib import admin

from api.forms import UserRoleAdminForm
from api.models.authorization import Permission, RolePermission, Roles, UserRole
from api.models.clients import EstateClients
from api.models.properties import Properties
from api.models.realtors import Realtors, Referrals
from api.models.users import User

# Register your models here.


admin.site.register(User)
@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    list_display = ("name", "description")

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("name", "description")

@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ["role"]



@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ("user", "role")
    
    # form = UserRoleAdminForm


@admin.register(Realtors)
class RealtorAdmin(admin.ModelAdmin):
    pass



@admin.register(EstateClients)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(Properties)
class PropertyAdmin(admin.ModelAdmin):
    pass

@admin.register(Referrals)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ['realtor', 'sponsor', 'referral_date']