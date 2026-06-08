from enum import Enum

from api.models.base import CustomBaseModel
from api.models.users import User
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from api.schema.usersSchema import RealtorReferralSerializer, RealtorReferralSerializer2, RealtorSerializer


    
    


class EstateClients(User):
    pass
    
    class Meta:
        verbose_name="Clients"
        verbose_name_plural = "Clientss"
        
        
    def __str__(self):
        return self.get_fullname() + " - Clients"
    
    

                
      
      
      
        