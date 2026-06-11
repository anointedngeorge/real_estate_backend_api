
from django.contrib import admin
from django.urls import path

from api.routers import api
from api.views.n8n_views.routers import n8n_api


urlpatterns = [
    path('admin/', admin.site.urls),
     path('api/v1/', api.urls, name="api.backend"),
     path('api/n8n/v1/', n8n_api.urls, name="api.n8n"),
]
