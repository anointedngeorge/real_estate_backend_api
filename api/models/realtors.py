from enum import Enum

from api.models.base import CustomBaseModel
from api.models.users import User
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from api.schema.usersSchema import (
    RealtorReferralSerializer,
    RealtorReferralSerializer2,
    RealtorSerializer,
    RealtorSerializer_,
)


class BankNameChoices(models.TextChoices):
    UBA = "UBA", "UBA"
    FCMB = "FCMB", "FCMB"
    WEMA = "WEMA", "Wema Bank"
    OPAY = "OPAY", "OPay"
    MONIEPOINT = "MONIEPOINT", "Moniepoint"


class Realtors(User):
    referral_code = models.CharField(max_length=255, null=True, blank=True)
    is_realtor = models.BooleanField(default=True)

    bank_name = models.CharField(
        max_length=200, choices=BankNameChoices, blank=True, null=True
    )
    account_name = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="Account Name"
    )
    bank_number = models.CharField(max_length=200, blank=True, null=True)
    bank_type = models.CharField(
        max_length=200,
        choices=[("savings", "Savings"), ("current", "Current")],
        default="savings",
    )

    address = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Realtors"
        verbose_name_plural = "Realtors"

    def __str__(self):
        return self.get_fullname() + " - Realtor"

    def referral_link(self):
        pass

    def paid_commission(self):
        # Implement logic to calculate and mark commissions as paid
        pass

    def unpaid_commission(self):
        # Implement logic to calculate and mark commissions as unpaid
        pass

    def total_sales_amount(self):
        # Implement logic to calculate total sales amount
        pass

    @property
    def referralList(self):
        try:
            realtor_node = Referrals.objects.select_related(
                "realtor",
                "sponsor__realtor",
            ).get(realtor=self)

            sponsor = (
                realtor_node.sponsor.realtor
                if realtor_node.sponsor
                else None
            )

            return {
                "realtor": self,
                "sponsor": (
                    RealtorSerializer_
                    .model_validate(sponsor)
                    .model_dump()
                    if sponsor
                    else None
                ),
            }

        except Referrals.DoesNotExist:
            return {
                "realtor": self,
                "sponsor": None,
            }


class Referrals(MPTTModel, CustomBaseModel):
    # implement referral system using mptt to create a tree structure for referrals

    realtor = models.ForeignKey(
        Realtors, on_delete=models.CASCADE, related_name="referrals"
    )
    sponsor = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    referral_date = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        parent_attr = "sponsor"
        order_insertion_by = ["id"]

    def __str__(self):
        return f"{self.realtor} referred by {self.sponsor if self.sponsor else 'None'} "

    def _uplines(self, generations=3):
        return self.get_ancestors().order_by("-level")[:generations]

    def _downlines(self, generations=3):
        return self.get_descendants().filter(level__lte=self.level + generations)


class Commission(CustomBaseModel):
    upfront_amount = models.DecimalField(max_digits=10, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    realtor = models.ForeignKey(
        Realtors, on_delete=models.CASCADE, related_name="commissions"
    )
    is_paid = models.BooleanField(default=False)
    sale_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    sale_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Commission for {self.realtor.get_fullname()} - {'Paid' if self.is_paid else 'Unpaid'}"
