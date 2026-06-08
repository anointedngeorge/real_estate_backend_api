import uuid

from django.db import models



class CustomBaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_date = models.DateField(auto_now=True)
    created_date_time = models.DateTimeField( auto_now=True)