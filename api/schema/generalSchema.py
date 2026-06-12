from datetime import date, datetime
from datetime import time
from typing import Any, Dict, List, Literal, Optional, Union
import uuid
from ninja import Schema, Field
from pydantic import BaseModel, EmailStr
import re




class SettingsSerializer(Schema):
    data: str
    
    

class ResultSerializer(BaseModel):
    data: Any
    status: bool
    status_code: int
    message: str
    
    

StatusType = Literal['available', 'sold', 'reserved']
PropertyTypes = Literal['land','house','apartment', 'commercial']
class PropertySchema(Schema):
    name: str
    image: str
    description: str
    location: str
    
    class Config:
        from_attributes = True



class ClientSerializer(BaseModel):
    id: uuid.UUID
    email: str
    first_name: str
    last_name: str

    
    class Config:
        from_attributes = True




class RealtorSerializer(BaseModel):
    id: uuid.UUID
    email: str
    first_name: str
    last_name: str
    referral_code: str
    
    class Config:
        from_attributes = True

 
 
plan = Literal['6', '3', '12', 'outright']
status = Literal['in_progress', 'failed', 'cancelled', 'reversed', 'in-progress']

class SalesInSchema(BaseModel):
    properties_id : uuid.UUID
    client : EmailStr
    realtor : EmailStr
    payment_plan : plan
    status : status
    amount : float
    
    class Config:
        from_attributes = True



class SalesOutSchema(BaseModel):
    id: uuid.UUID
    properties : PropertySchema
    client : ClientSerializer = None
    realtor : RealtorSerializer = None
    payment_plan : plan
    status : status
    amount : float
    sales_date: date
    sales_date_time: time
    year: int
    month: int
    commission: Dict[str, Any] = None
    
    class Config:
        from_attributes = True
        


class SalesOutSchema2(BaseModel):
    page: int
    count: int
    items: List[SalesOutSchema] = []
    stats: Dict

