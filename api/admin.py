from django.contrib import admin

from api.forms import UserRoleAdminForm
from api.models.authorization import Permission, RolePermission, Roles, UserRole
from api.models.clients import EstateClients
from api.models.properties import Properties, PropertyPlots
from api.models.realtors import Realtors, Referrals
from api.models.sales import Sales, SalesPaymentPlan, SalesPlot
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


@admin.register(PropertyPlots)
class PropertiesPlotsAdmin(admin.ModelAdmin):
    pass


@admin.register(Referrals)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ["realtor", "sponsor", "referral_date"]


@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    pass


@admin.register(SalesPlot)
class SalesPlotsAdmin(admin.ModelAdmin):
    pass


@admin.register(SalesPaymentPlan)
class SalesPaymentPlanAdmin(admin.ModelAdmin):
    list_display = [
        "sales",
        "billing_name",
        "billing_amount_to_pay",
        "billing_name",
        "billing_period_number",
        "billing_date",
        'amount',
        'status'
    ]
