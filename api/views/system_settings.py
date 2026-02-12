from django.contrib import admin
from django.urls import path
from ninja import  Router

from api.lib.message import XResponse
from api.models.system_settings import SystemSettings
from api.schema.generalSchema import SettingsSerializer
from django.db import transaction

import json

router = Router(tags=["System Settings"])



@router.post("/settings")
def save_system_settings(request, data: SettingsSerializer):
    try:
        user = request.auth
        payload = json.loads(data.data)
    
        with transaction.atomic():
            for name, description in payload.items():
                SystemSettings.objects.update_or_create(
                    name=name,
                    defaults={"description": description},
                )
                
        return XResponse(
                status_code=200,
                data=None,
                message="Successful",
                status=True,
            ).response
    except Exception as e:
         return XResponse(
                status_code=400,
                data=None,
                message="An error occurred while updating user",
                status=False,
            ).response



@router.get("/settings")
def get_system_settings(request):
    try:
        # user = request.auth
        system_settings = SystemSettings.objects.all()
        
        data_formatted = {data.name:data.description for data in system_settings}    
        return XResponse(
                    status_code=200,
                    data=data_formatted,
                    message="Fetched Successful",
                    status=True,
                ).response
    except:
        return XResponse(
                    status_code=400,
                    data=None,
                    message="Error Occurred",
                    status=False,
                ).response