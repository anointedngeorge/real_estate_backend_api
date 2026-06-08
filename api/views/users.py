from typing import List
from unicodedata import name
import uuid
from django.contrib import admin
from django.urls import path
from ninja.pagination import paginate, PageNumberPagination, LimitOffsetPagination
from ninja import  Router, Query, Field, Schema
from django.db.models import F, Q, Sum
from django.core.paginator import Paginator
from api.lib.message import XResponse
from api.models.authorization import RolePermission
from api.models.users import User
from api.schema.generalSchema import ResultSerializer
from api.schema.usersSchema import ListUserPaginatorSerializer, ListUserRolePermissions, ListUserSerializer, UserSerializer, UserUpdateSerializer, UserUpdateSerializer2
from django.shortcuts import get_object_or_404


router = Router(tags=["users"])


class UsersQuery(Schema):
    # role:str=None
    id:uuid.UUID=None
    page:int = 1
    size: int = 10
    exclude_users_roles:str=Field(default=None)


@router.get("/list", response=ListUserPaginatorSerializer)
# @paginate(PageNumberPagination, pass_parameter="pagination_info")
def list_users(request, query: UsersQuery = Query(...), **kwargs):
    try:
        page= query.page
        size = query.size
        
        
        model= User
        filters = Q()
        exclude_role_list = []

        if query.id:
            filters &= Q(id=query.id)

        if query.exclude_users_roles:
            # 
            exclude_roles = [
                r.strip()
                for r in query.exclude_users_roles.split(",")
            ]
            exclude_role_list = exclude_roles

        qs = model.objects.filter(filters).exclude(role__in=exclude_role_list)
        paginator = Paginator(qs, size)
        page_obj = paginator.get_page(page)
        
        count = paginator.count
        
        return {
            "page": page,
            "count": count,
            "stats": {},
            "items": list(page_obj.object_list),
        }
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return XResponse(
            status_code=400,
            data=None,
            message="An error occurred",
            status=False,
        ).response
        



@router.get("/userRolePermissions", response=List[ListUserRolePermissions])
def list_user_role_permissions(request, user_id: uuid.UUID):
    try:
        user = get_object_or_404(User, pk=user_id)
        role_permissions = RolePermission.objects.filter(role__name=user.role).first()
        
        if role_permissions:
            permissions = role_permissions.permissions.all()
            user_permissions = [{"id": perm.id, "name": perm.name} for perm in permissions]
            
            return XResponse(
                status_code=200,
                data=user_permissions,
                message="User role permissions retrieved successfully",
                status=True,
            ).response
        else:
            return XResponse(
                status_code=404,
                data=None,
                message="Role permissions not found",
                status=False,
            ).response
            
    except Exception as e:
        print(e)
        return XResponse(
            
            status_code=400,
            data=None,
            message="An error occurred",
            status=False,
        ).response



@router.put("/update", response=ResultSerializer)
def update_users(request, data: UserUpdateSerializer2 ):
    try:
        user = get_object_or_404(User, pk=data.user_id)
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
            message=f"{e.text_message if hasattr(e, 'text_message') else 'An error occurred'}",
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
            message=f"{e}",
            status=False,
        ).response
        
        
@router.delete("/removePermission")
def delete_user_permission(request, user_id:uuid.UUID, perm:str ):
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
            message=f"{e}",
            status=False,
        ).response
        
        


