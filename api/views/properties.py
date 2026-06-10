from enum import Enum
from random import shuffle
from typing import List, Optional
import uuid
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import F, Q, Sum
from ninja.pagination import paginate, PageNumberPagination
from ninja import Form, Router, Query, Field, Schema

from api.lib.message import XResponse
from api.models.properties import Properties
from api.models.realtors import Realtors, Referrals
from api.models.users import User
from api.schema.generalSchema import ResultSerializer
from api.schema.usersSchema import (
    PropertyListResponse,
    PropertyListSchema,
    PropertySchema,
    PropertyUpdateSerializer2,
    RealtorReferralSerializer,
    XResponseData,
    XResponseSchema,
)
from django.shortcuts import get_object_or_404


router = Router(tags=["Property Management"])


# services import


def slug(text):
    return (
        f"{text}"
        .lower()
        .replace(" ", "")
        + uuid.uuid4().hex[:6].upper()
    )

@router.post(
    "/create_property",
    response={
        200: XResponseData ,
        400: XResponseSchema,
        # RealtorSerializer
    },
)
@transaction.atomic
def create_new_property(request, data: PropertySchema):
    try:
        model = Properties
        payload = data.model_dump()
        payload.update({
            "slug": slug(text=data.name)
        })
        new_property = model.objects.create(**payload)
    
        dt = PropertySchema.model_validate(new_property).model_dump()
        return XResponse(
            status_code=200,
            data=dt,
            message=f"New Property ({new_property.name}) created successfully",
            status=True,
        ).response

    except Exception as e:
        return XResponse(
            status_code=400,
            data=None,
            message=str(e),
            status=False,
        ).response





class UsersQuery(Schema):
    status:Optional[str]=None
    property_types:Optional[str] = None
    id: Optional[uuid.UUID] = None
    size:int = 10 
    page: int = 1

@router.get("/list", response=PropertyListResponse)
# @paginate(PageNumberPagination, pass_parameter="pagination_info")
def list_properties(request, query: UsersQuery = Query(...)):
    size = query.size
    page = query.page
    try:
        filters = Q()
        model = Properties
        if query.id:
            filters &= Q(id=query.id)

        if query.property_types:
            filters &= Q(property_types=query.property_types)

        if query.status:
            filters &= Q(status=query.status)

        qs= model.objects.filter(filters)
        paginator = Paginator(qs, size)
        page_obj = paginator.get_page(page)

        count = paginator.count
        # apply paginator using from django.core.paginator import Paginator
        return {
            "page": page,
            "count": count,
            "stats": {
                "total": count,
                "sold": qs.filter(status="sold").count(),
                "available": qs.filter(status="available").count(),
                "price_summation": qs.aggregate(total=Sum('actual_price')).get('total', 0.0)
            },
            "items": list(page_obj.object_list),
        }
    
    except Exception as e:
        return XResponse(
            status_code=400,
            data=None,
            message=str(e),
            status=False,
        ).response


@router.put("/update", response=ResultSerializer)
def update_users(request, data: PropertyUpdateSerializer2):
    try:
        user = get_object_or_404(Properties, pk=data.id)
        
        # # remove None values only
        payload = {k: v for k, v in data.data.model_dump(exclude_none=True).items() if v !=  ""}

        print(payload, 'loading...')
        for attr, value in payload.items():
            setattr(user, attr, value)

        user.save()
        u = PropertySchema.model_validate(user).model_dump()

        return XResponse(
            status_code=200,
            data=u,
            message="Updated",
            status=True,
        ).response

    except Exception as e:
        return XResponse(
            status_code=400,
            data=None,
            message=f"{e.text_message if hasattr(e, 'text_message') else 'An error occurred'}",
            status=False,
        ).response


@router.delete("/delete")
def delete_user(request, realtor_id: uuid.UUID):
    try:

        prop = get_object_or_404(Properties, pk=realtor_id)
        prop.delete()
        return XResponse(
            status_code=200,
            data=None,
            message="Property deleted",
            status=True,
        ).response

    except Exception as e:
        return XResponse(
            status_code=400,
            data=None,
            message=f"{e}",
            status=False,
        ).response


