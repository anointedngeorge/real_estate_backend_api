from datetime import date, datetime
from datetime import time
from typing import Any, Dict, List, Literal, Optional, Union
import uuid
from ninja import Schema, Field
from pydantic import BaseModel, EmailStr
import re

from api.schema.usersSchema import RealtorReferralSerializer2




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
    actual_price : Union[float, int] = 0.0
    selling_price : Union[float, int] = 0.0
    
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
    referralList: Optional[RealtorReferralSerializer2] = None
    
    class Config:
        from_attributes = True

 
 
plan = Literal['installment', 'outright']
status = Literal['in_progress', 'failed', 'cancelled', 'reversed', 'in-progress']

class SalesInSchema(BaseModel):
    properties_id : uuid.UUID
    client : EmailStr
    realtor : EmailStr
    payment_plan : plan
    status : status
    amount : float
    plots : list = []
    
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
    payment_plan_list: List = []
    commission: Dict[str, Any] = None
    
    class Config:
        from_attributes = True
        


class SalesOutSchema2(BaseModel):
    page: int
    count: int
    items: List[SalesOutSchema] = []
    stats: Dict
    

class SalesPaymentPlanInSchema(BaseModel):
    sales_id:uuid.UUID
    billing_name: str
    billing_period_number:int
    billing_dates: List
    
    class Config:
        from_attributes = True


class SalesPaymentPlanInSchema2(BaseModel):
    sales_id:uuid.UUID
    billing_name: str
    billing_period_number:int
    billing_date: str
    billing_amount_to_pay: int = 0
    
    class Config:
        from_attributes = True

class SalesPaymentPlanOutSchema(BaseModel):
    id:uuid.UUID
    # sales:Optional[SalesOutSchema] = None
    billing_name: str
    billing_period_number:int
    billing_date: str
    billing_amount_to_pay: float = 00
    amount: float
    status: Literal['pending', 'completed'] = "pending"
    
    class Config:
        from_attributes = True
  
  
class SalesPaymentPlanUpdateSchema(BaseModel):
    sales_id: str
    id:str
    billing_amount_to_pay: float
    billing_date: str
    
    class Config:
        from_attributes = True      
