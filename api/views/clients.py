from enum import Enum
from random import shuffle
from typing import List
import uuid
from django.db import transaction
from django.core.paginator import Paginator
from ninja.pagination import paginate, PageNumberPagination
from ninja import Form, Router, Query, Field, Schema
from django.db.models import F, Q, Sum
from api.lib.message import XResponse
from api.models.clients import EstateClients
from api.schema.usersSchema import (
    ClientPaginationSerializer,
    ClientSerializer,
    ClientSignupSerializer,
    ClientUpdateSerializer2,
    XResponseData,
    XResponseSchema,
)
from django.shortcuts import get_object_or_404


router = Router(tags=["Client's Management"])


# services import

def username(first_name, last_name):
    initials = (
        first_name[:2] + last_name[:2]
    ).upper()

    return f"{initials}{uuid.uuid4().hex[:8].upper()}"



@router.post(
    "/register_new_client",
    response={
        200: XResponseData ,
        400: XResponseSchema,
        # RealtorSerializer
    },
)
@transaction.atomic
def clients_auth_signup(request, data: ClientSignupSerializer):
    try:
        model = EstateClients
        
        if model.objects.filter(email=data.email).exists():
            return XResponse(
                status_code=400,
                data=None,
                message="Email already exists",
                status=False,
            ).response

        payload = data.model_dump()

        password = payload.pop("password")        

        uname = username(first_name=data.first_name, last_name=data.last_name)
        payload.update({
            'username': uname,
            'is_active': True,
            'is_staff': True,
            'role': 'buyer'
        })
        _client = model.objects.create(**payload)

        _client.set_password(password)
        _client.save()
    
            
        dt = ClientSerializer.model_validate(_client).model_dump()
        return XResponse(
            status_code=200,
            data=dt,
            message=f"Client {_client.username} created successfully",
            status=True,
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


@router.get("/list", response=ClientPaginationSerializer)
# @paginate(PageNumberPagination, pass_parameter="pagination_info")
def list_clients(request, query: UsersQuery = Query(...)):
    try:
        page = query.page
        size = query.size
        
        
        filters = Q()
        model = EstateClients

        if query.id:
            filters &= Q(id=query.id)

        qs = model.objects.filter(filters)
        paginator = Paginator(qs, size)
        page_obj = paginator.get_page(page)
        
        count = paginator.count
        return {
            "page": page,
            "count": count,
            "stats": {
                "total": count,
                "total_spent": 3000000,
                "outstanding_balance": 4500000,
                "properties_sold":34
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


@router.put("/update", response=ClientSerializer)
def update_users(request, data: ClientUpdateSerializer2):
    try:
        model = EstateClients
        user = get_object_or_404(model, pk=data.user_id)
        # # remove None values only
        payload = {k: v for k, v in data.data.model_dump(exclude_none=True).items()}

        for attr, value in payload.items():
            setattr(user, attr, value)

        user.save()
        u = ClientSerializer.model_validate(user).model_dump()

        return XResponse(
            status_code=200,
            data=u,
            message="client Updated",
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

        user = get_object_or_404(EstateClients, pk=realtor_id)
        user.delete()
        return XResponse(
            status_code=200,
            data=None,
            message="User deleted",
            status=True,
        ).response

    except Exception as e:
        return XResponse(
            status_code=400,
            data=None,
            message=f"{e}",
            status=False,
        ).response



