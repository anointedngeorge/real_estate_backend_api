from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from api.config.base import BaseModel
from api.models.properties import PropertyPlots
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

from api.schema.generalSchema import SalesPaymentPlanOutSchema


class PaymentPlan(models.TextChoices):
    "installment", "Installment"
    "outright", "Outright"


class Status(models.TextChoices):
    "in_progress", "In Progress"
    "failed", "Failed"
    "completed", "completed"
    "cancelled", "Cancelled"
    "reversed", "Reversed"


class Sales(BaseModel):
    properties = models.ForeignKey(
        "api.Properties",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sale_property",
    )
    client = models.ForeignKey(
        "api.EstateClients",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sales_client",
    )
    realtor = models.ForeignKey(
        "api.Realtors",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sales_realtor",
    )

    payment_plan = models.CharField(max_length=150, choices=PaymentPlan)
    status = models.CharField(max_length=150, choices=Status)

    plots = models.CharField(max_length=150, default=None, blank=True, null=True)

    sales_date = models.DateField(auto_now_add=True)
    sales_date_time = models.TimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)

    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    on_promo = models.BooleanField(max_length=150, choices=[(True, "Yes"), (False, "No")], default=False)

    #
    def __str__(self):
        return f"{self.client} {self.properties.name}"

    def get_name(self):
        return f"{self.id} - {self.properties.name} "

    @property
    def commission(self):
        return {"direct": "9000", "upline": "78999"}

    @property
    def payment_plan_list(self):
        plans = self.sales_payment_plan.all()

        lst =  [
            SalesPaymentPlanOutSchema
            .model_validate(plan)
            .model_dump()
            for plan in plans
        ]
        return lst


class SalesPlot(BaseModel):
    sales = models.ForeignKey(
        "api.Sales", on_delete=models.CASCADE, related_name="sales_plots"
    )
    plots = models.ManyToManyField(PropertyPlots)

    def __str__(self):
        return f"{self.sales.client} {self.sales.properties.name}"




class SalesPaymentPlan(BaseModel):
    sales = models.ForeignKey("api.Sales", on_delete=models.CASCADE, related_name="sales_payment_plan")
    billing_name = models.CharField(max_length=250)
    billing_period_number = models.IntegerField( default=0)
    billing_date = models.CharField( max_length=100)
    billing_amount_to_pay = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    status = models.CharField(max_length=150, choices=[('pending', "Pending"), ('completed', 'Completed')], default="pending")

    
        
    def __str__(self):
        return f"{self.sales.properties.name} - {self.billing_name}"






class DateTracker(BaseModel):
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()

    class Meta:
        unique_together = ("year", "month")
