from enum import Enum
from random import shuffle
from typing import List
import uuid
from django.db import transaction
from ninja.pagination import paginate, PageNumberPagination
from ninja import Form, Router, Query, Field, Schema
from django.db.models import F, Q, Sum
from django.core.paginator import Paginator
from api.lib.message import XResponse
from api.models.realtors import Realtors, Referrals
from api.models.users import User
from api.schema.generalSchema import ResultSerializer
from api.schema.usersSchema import (
    ListUserSerializer,
    RealtorReferralSerializer,
    RealtorResponseSerializer,
    RealtorSerializer,
    RealtorSignupSerializer,
    RealtorUpdateSerializer,
    RealtorUpdateSerializer2,
    UserUpdateSerializer,
    UserUpdateSerializer2,
    XResponseData,
    XResponseSchema,
)
from django.shortcuts import get_object_or_404

from api.services.referral import ReferralService

router = Router(tags=["Realtors Management"])


# services import
referral_service = ReferralService


def username(first_name, last_name):
    return (
        f"{first_name}{last_name}"
        .lower()
        .replace(" ", "")
        + "_"
        + uuid.uuid4().hex[:6]
    )


def referral_code(first_name, last_name):
    initials = (
        first_name[:2] + last_name[:2]
    ).upper()

    return f"{initials}{uuid.uuid4().hex[:8].upper()}"



@router.post(
    "/register_new_realtor",
    response={
        200: XResponseData ,
        400: XResponseSchema,
        # RealtorSerializer
    },
)
@transaction.atomic
def realtors_auth_signup(request, data: RealtorSignupSerializer):
    try:
        if Realtors.objects.filter(email=data.email).exists():
            return XResponse(
                status_code=400,
                data=None,
                message="Email already exists",
                status=False,
            ).response

        payload = data.model_dump()

        password = payload.pop("password")
        sponsor_code = payload.pop("sponsor", None)
        
        
        referralCode = referral_code(
                    data.first_name,
                    data.last_name,
                )
        
        while Realtors.objects.filter(
                referral_code=referralCode
            ).exists():
                referralCode = referral_code(
                    data.first_name,
                    data.last_name,
                )

        payload.update(
            {
                "username": username(
                    data.first_name,
                    data.last_name,
                ),
                "referral_code": referralCode,
                "role": "agent",
                "is_realtor": True,
                "has_agreed_terms": True,
            }
        )

        realtor = Realtors.objects.create(**payload)

        realtor.set_password(password)
        realtor.is_active = True
        realtor.is_staff = True
        realtor.save()
        
        if sponsor_code:
            sponsor = referral_service.confirm_referral_code(referral_code=sponsor_code)

            Referrals.objects.get_or_create(
                realtor=realtor,
                sponsor=sponsor,
            )
            
        dt = RealtorSerializer.model_validate(realtor).model_dump()
        return XResponse(
            status_code=200,
            data=dt,
            message=f"Realtor {realtor.username} created successfully",
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
    # role:str=None
    id: uuid.UUID = None
    page: int = 1
    size: int = 10
    exclude_users_roles: str = Field(default=None)


@router.get("/list", response=RealtorResponseSerializer)
# @paginate(PageNumberPagination, pass_parameter="pagination_info")
def list_realtors(request, query: UsersQuery = Query(...)):
    try:
        page = query.page
        size = query.size
        
        model = Realtors
        filters = Q()
        
        
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
                "total_sales": 230000,
                "total_commission": 1500000,
                "commission_rules": ""
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


@router.put("/update", response=ResultSerializer)
def update_users(request, data: RealtorUpdateSerializer2):
    try:
        user = get_object_or_404(Realtors, pk=data.user_id)
        # # remove None values only
        payload = {k: v for k, v in data.data.model_dump(exclude_none=True).items()}

        for attr, value in payload.items():
            setattr(user, attr, value)

        user.save()
        u = RealtorReferralSerializer.model_validate(user).model_dump()

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

        user = get_object_or_404(Realtors, pk=realtor_id)
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


class ReferralType(str, Enum):
    UPLINE = "upline"
    DOWNLINE = "downline"


class UsersQuery2(Schema):
    realtor_id: uuid.UUID
    referral_type: ReferralType = ReferralType.UPLINE


# @router.get("/list", response=List[RealtorSerializer])
# @paginate(PageNumberPagination, pass_parameter="pagination_info")
# def list_realtor_referrals(request, query: UsersQuery2 = Query(...)):
#     try:
#         realtor = Realtors.objects.all()
#         result = None

#         if query.referral_type == "upline":
#             pass
#             # upline fn

#         elif query.referral_type == "downline":
#             pass

#         return realtor

#     except Exception as e:
#         return XResponse(
#             status_code=400,
#             data=None,
#             message="An error occurred",
#             status=False,
#         ).response
