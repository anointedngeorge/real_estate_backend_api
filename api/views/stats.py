from enum import Enum
from random import shuffle
from typing import List
import uuid
from django.db import transaction
from ninja.pagination import paginate, PageNumberPagination
from ninja import Form, Router, Query, Field, Schema

from api.lib.message import XResponse
from api.models.realtors import Realtors, Referrals
from api.models.users import User
from api.schema.generalSchema import ResultSerializer
from api.schema.usersSchema import XResponseData
from django.shortcuts import get_object_or_404

from api.services.referral import ReferralService

router = Router(tags=["Realtors Management"])


@router.put("/analytics", response=XResponseData)
def dashboard_analytics(request):
    try:

        stats = {
            "total_properties": {
                "total": 145,
                "increase": "12%",
                "name": "Total Properties",
            },
            "total_revenue": {
                "total": 2345554344,
                "increase": "18%",
                "name": "Total Revenue",
            },
            "pending_payments": {
                "total": 32,
                "completed_payment": 220,
                "name": "Pending Payments",
            },
            "active_realtors": {
                "total": 145,
                "increase": "12%",
                "clients": 312,
                "name": "Active Realtors",
            },
            "monthly_sales": {"total": 12, "increase": "+12%", "name": "Monthly Sales"},
            "yearly_sales": {"total": 43, "name": "Yearly Sales"},
            "commissioned_paid": {"total": 23000000, "name": "Commissioned Paid"},
            "unpaid_commission": {"total": 3230000, "name": "Unpaid Commission"},
            "sales_trend": {
                "name": "Sales Trend",
                "data": {
                    "vertical": ["0M", "7M", "14M", "21M","28M"],
                    "horizontal": [
                        "Jan",
                        "Feb",
                        "Mar",
                        "Apr",
                        "May",
                        "Jun",
                        "Jul",
                        "Aug",
                        "Sep",
                        "Oct",
                        "Nov",
                        "Dec",
                    ],
                },
            },
            "commission_distribution": {
                "direct": {"total": 2908888 , "percentage": "2%"},
                "indirect": {"total": 900000,  "percentage": "10%"},
                'company': {"total":2300000, "percentage": "79%"}
            },
           "payment_compliance": {
               'paid': 98,
               'due': 30,
               'overdue': 60
           }

        }

        return XResponse(
            status_code=200,
            data=stats,
            message="Dashboard Analytics",
            status=True,
        ).response

    except Exception as e:
        return XResponse(
            status_code=400,
            data=None,
            message=f"{e.text_message if hasattr(e, 'text_message') else 'An error occurred'}",
            status=False,
        ).response
