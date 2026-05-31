from typing import List
import uuid
from django.contrib import admin
from django.urls import path
from ninja.pagination import paginate, PageNumberPagination, LimitOffsetPagination
from ninja import  Router, Query, Field, Schema

from api.lib.message import XResponse
from api.models.users import User
from api.schema.generalSchema import ResultSerializer
from api.schema.usersSchema import ListUserSerializer, UserSerializer, UserUpdateSerializer, UserUpdateSerializer2
from django.shortcuts import get_object_or_404


router = Router(tags=["users"])


class UsersQuery(Schema):
    # role:str=None
    id:uuid.UUID=None
    exclude_users_roles:str=Field(default=None)


@router.get("/list", response=List[ListUserSerializer])
@paginate(PageNumberPagination, pass_parameter="pagination_info")
def list_users(request, query: UsersQuery = Query(...), **kwargs):
    try:
        users = User.objects.all()

        if query.id:
            users = users.filter(id=query.id)

        if query.exclude_users_roles:
            # 
            exclude_roles = [
                r.strip()
                for r in query.exclude_users_roles.split(",")
            ]
            users = users.exclude(role__in=exclude_roles)

        return users
    
    except Exception as e:
        return XResponse(
            status_code=400,
            data=None,
            message="An error occurred",
            status=False,
        ).response
        


@router.put("/update", response=ResultSerializer)
def update_users(request, data: UserUpdateSerializer2 ):
    try:
        user = User.objects.get(id=data.user_id)
        
        # # remove None values only
        payload = {
            k: v for k, v in data.data.model_dump(exclude_none=True).items()
        }

        for attr, value in payload.items():
            setattr(user, attr, value)

        user.save()
        u  = UserUpdateSerializer.model_validate(user).model_dump_json()
        
        
        
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
            message="An error occurred",
            status=False,
        ).response


@router.delete("/delete")
def delete_user(request, user_id:uuid.UUID ):
    try:
        
        user = get_object_or_404(User, pk=user_id)
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
            message="An error occurred",
            status=False,
        ).response