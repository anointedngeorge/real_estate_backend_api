from enum import Enum
from random import shuffle
from typing import List
import uuid
from django.db import transaction
from django.core.paginator import Paginator
from django.utils import timezone
from ninja.pagination import paginate, PageNumberPagination
from ninja import Form, Router, Query, Field, Schema
from django.db.models import F, Q, Sum
from api.lib.message import XResponse
from api.models.clients import EstateClients
from api.models.realtors import Realtors
from api.models.sales import DateTracker, Sales
from api.models.users import User
from api.schema.generalSchema import SalesInSchema, SalesOutSchema, SalesOutSchema2
from api.schema.usersSchema import (
    XResponseData,
    XResponseSchema,
)
from django.shortcuts import get_object_or_404

router = Router(tags=["Sales Management"])


@router.post(
    "/create_new_sales",
    response={
        200: XResponseData,
        400: XResponseSchema,
        # RealtorSerializer
    },
)
@transaction.atomic
def create_new_sales(request, data: SalesInSchema):
    try:
        client = EstateClients.objects.get(email=data.client)
        realtor = Realtors.objects.get(email=data.realtor)

        payload = data.model_dump(exclude={"client", "realtor"})

        # set year
        year = timezone.now().year
        month = timezone.now().month

        sale = Sales.objects.create(
            **payload, client=client, realtor=realtor, year=year, month=month
        )

        if sale:
            # create date tracker
            DateTracker.objects.get_or_create(
                year=timezone.now().year, month=timezone.now().month
            )

        return XResponse(
            status_code=200,
            data=SalesOutSchema.model_validate(sale).model_dump(),
            message=f"Sales {sale.get_name()} created successfully",
            status=True,
        ).response

    except EstateClients.DoesNotExist:
        return XResponse(
            status_code=404,
            data=None,
            message="Client not found",
            status=False,
        ).response

    except Realtors.DoesNotExist:
        return XResponse(
            status_code=404,
            data=None,
            message="Realtor not found",
            status=False,
        ).response

    except Exception as e:
        return XResponse(
            status_code=400,
            data=None,
            message=str(e),
            status=False,
        ).response


# listing clients
class UsersQuery(Schema):
    id: uuid.UUID = None
    page: int = 1
    size: int = 10


@router.get("/list", response=SalesOutSchema2)
def list_sales(request, query: UsersQuery = Query(...)):
    try:
        page = query.page
        size = query.size

        filters = Q()
        model = Sales

        if query.id:
            filters &= Q(id=query.id)

        qs = model.objects.filter(filters)
        paginator = Paginator(qs, size)
        page_obj = paginator.get_page(page)

        count = paginator.count
        month_list = [
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
        ]

        return {
            "page": page,
            "count": count,
            "stats": {
                "total": count,
                "total_revenue": 3000000,
                "total_commission": 4500000,
                "average": 34,
                "total_sales": 34,
                "month_sales_performance": [
                    {"month": "Jan", "sales": 2, "revenue": 180000000},
                    {"month": "Feb", "sales": 12, "revenue": 245000000},
                    {"month": "Mar", "sales": 15, "revenue": 320000000},
                    {"month": "Apr", "sales": 10, "revenue": 210000000},
                    {"month": "May", "sales": 18, "revenue": 420000000},
                    {"month": "Jun", "sales": 14, "revenue": 310000000},
                    {"month": "Jul", "sales": 22, "revenue": 485000000},
                    {"month": "Aug", "sales": 19, "revenue": 390000000},
                    {"month": "Sep", "sales": 16, "revenue": 350000000},
                    {"month": "Oct", "sales": 25, "revenue": 520000000},
                    {"month": "Nov", "sales": 20, "revenue": 445000000},
                    {"month": "Dec", "sales": 12, "revenue": 280000000},
                ]
            },
            "items": list(page_obj.object_list),
        }

    except Exception as e:
        return XResponse(
            status_code=400,
            data=None,
            message="An error occurred",
            status=False,
        ).response
