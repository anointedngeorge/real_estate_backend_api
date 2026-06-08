from datetime import date, datetime
from enum import Enum
from typing import Annotated, Any, Dict, List, Literal, Optional, Union
import uuid
from ninja import Schema, Field
from pydantic import BaseModel, EmailStr, WithJsonSchema
import re



class LoginSchema(Schema):
    access_token: str
    refresh_token:str
    jti:str

class LoginSerializer(Schema):
    username: str
    password: str= Field(..., min_length=8)
    
    
    @staticmethod
    def resolve_username(cls, context):
        # print("Resolving username with data:", cls)
        
        if not cls.get("username").find("@") != -1:
            raise ValueError("Username must be an email address")
        
        if not cls.get("username"):
            raise ValueError("Username is required")

        if not re.match(r"^[\w.@+-]+$", cls.get("username")):
            raise ValueError(
                "Username can only contain letters, digits, and @/./+/-/_ characters"
            )

        return cls.get("username")
    
    
    @staticmethod
    def resolve_password(cls, context):
        
        if not cls.get('password'):
            raise ValueError("Password is required")
        
        return cls.get('password')




class SignupSerializer(Schema):
    first_name: str
    last_name: str
    phone_number: str = Field(..., pattern=r'^\+?1?\d{9,15}$')
    email: str
    password: str= Field(..., min_length=6, max_length=17)
    role : Optional[str] = Field(default="buyer", pattern="^(admin|agent|buyer|manager)$")
    has_agreed_terms: bool = Field(default=False, description="User must agree to terms and conditions")
    
    @staticmethod
    def resolve_email(cls, context):
        email = cls.get("email")
        
        if not email:
            raise ValueError("Email is required")
        
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            raise ValueError("Invalid email format")
        
        return email
    
    
    
class LoginTrackerSerializer(BaseModel):
    id: uuid.UUID
    agent: str
    location: str
    created_at: datetime
    platform: str



class UserSerializer(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    phone_number:Optional[str]=None
    date_joined: datetime
    login_histories: List[Dict[str, Any]] = []

    class Config:
        from_attributes = True



class ListUserSerializer(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    phone_number: Union[str, int, None] = None
    date_joined: datetime
    last_login: Union[datetime, None] = None
    is_active: bool = False
    permissions: Dict[str, List] = {"permissions": [], "extra_permissions": []}
    login_histories: List[Dict[str, Any]] = []
    
    
    class Config:
        from_attributes = True        


class ListUserPaginatorSerializer(BaseModel):
    items: List[ListUserSerializer]
    page: int
    count: int
    stats: Dict = {}
    

class ListUserRolePermissions(BaseModel):
    id: uuid.UUID
    username: str
    
    class Config:
        from_attributes = True        


class UserUpdateSerializer(BaseModel):
    first_name: str = None
    last_name: str = None
    role:str = None
    
    phone_number:str = Field(None, pattern=r'^\+?1?\d{9,15}$')

    class Config:
        from_attributes = True


class UserUpdateSerializer2(BaseModel):
    user_id: uuid.UUID
    data: UserUpdateSerializer
        



class XResponseData(BaseModel):
    message: Optional[str] = None
    status_code: int = 200
    data: Union[dict, list, str, None] = None
    status: str = "success"



class XResponseSchema(BaseModel):
    status: bool
    data: XResponseData
    




# *** realtors schema ***


class RealtorSignupSerializer(Schema):
    first_name: str
    last_name: str
    phone_number: str = Field(..., pattern=r'^\+?1?\d{9,15}$')
    email: EmailStr
    password: str= Field(..., min_length=6, max_length=17)
    sponsor: str = None
    
    

    @staticmethod
    def resolve_email(cls, context):
        email = cls.get("email")
        
        if not email:
            raise ValueError("Email is required")
        
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            raise ValueError("Invalid email format")
        
        return email
    
    
    

class RealtorSerializer(BaseModel):
    id: uuid.UUID
    email: str
    first_name: str
    last_name: str
    phone_number:Optional[str]=None
    date_joined: datetime
    login_histories: List[Dict[str, Any]] = []
    permissions: Dict[str, List] = {"permissions": [], "extra_permissions": []}
    referral_code: str
    
    class Config:
        from_attributes = True
        

class RealtorSerializer_(BaseModel):
    # id: uuid.UUID
    # email: str
    first_name: str
    last_name: str
    account_name: Optional[str] = None
    bank_name : Optional[str] = None
    bank_type: Optional[str] = None
    bank_number: Optional[str] = None
    # phone_number:Optional[str]=None
    # referral_code: str
    
    class Config:
        from_attributes = True


class RealtorReferralSerializer2(BaseModel):
    id: uuid.UUID = None
    realtor: RealtorSerializer_ = None
    sponsor: List[RealtorSerializer_] = []


class RealtorReferralSerializer(BaseModel):
    id: uuid.UUID
    email: str
    first_name: str
    role: str
    last_name: str
    phone_number:Optional[str]=None
    date_joined: datetime
    login_histories: List[Dict[str, Any]] = []
    permissions: Dict[str, List] = {"permissions": [], "extra_permissions": []}
    referral_code: str
    username: str
    account_name: Optional[str] = None
    bank_name : Optional[str] = None
    bank_type: Optional[str] = None
    bank_number: Optional[str] = None
    referralList: List[RealtorReferralSerializer2] = []
    

    class Config:
        from_attributes = True
        
class RealtorResponseSerializer(BaseModel):
    items: List[RealtorReferralSerializer]
    page: int
    count: int
    stats: Dict




class RealtorUpdateSerializer(BaseModel):
    first_name: str = None
    last_name: str = None
    role:str = None
    
    account_name: Optional[str] = None
    bank_name : Optional[str] = None
    bank_type: Optional[str] = None
    bank_number: Optional[str] = None
    
    phone_number:str = Field(None, pattern=r'^\+?1?\d{9,15}$')

    class Config:
        from_attributes = True


class RealtorUpdateSerializer2(BaseModel):
    user_id: uuid.UUID
    data: RealtorUpdateSerializer
    
    




# *** Clients ***



class ClientSignupSerializer(Schema):
    first_name: str
    last_name: str
    phone_number: str = Field(..., pattern=r'^\+?1?\d{9,15}$')
    email: EmailStr
    password: str= Field(..., min_length=6, max_length=17)
    

    @staticmethod
    def resolve_email(cls, context):
        email = cls.get("email")
        
        if not email:
            raise ValueError("Email is required")
        
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            raise ValueError("Invalid email format")
        
        return email
    

class ClientSerializer(BaseModel):
    id: uuid.UUID
    email: str
    first_name: str
    last_name: str
    username:str
    is_active:bool= False
    phone_number:Optional[str]=None
    date_joined: datetime
    # login_histories: List[Dict[str, Any]] = []
    # permissions: Dict[str, List] = {"permissions": [], "extra_permissions": []}
    role: str
    
    class Config:
        from_attributes = True


class ClientPaginationSerializer(BaseModel):
    items: List[ClientSerializer]
    page: int
    count: int
    stats: Dict = {}


class ClientUpdateSerializer(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number:Optional[str]=None
    
    class Config:
        from_attributes = True



class ClientUpdateSerializer2(BaseModel):
    user_id: uuid.UUID
    data: ClientUpdateSerializer
    



# properties schema
StatusType = Literal['available','sold', 'reserved']
PropertyTypes = Literal['land','house','apartment', 'commercial']
class PropertySchema(Schema):
    name: str
    image: str
    description: str
    location: str
    status: StatusType
    property_types: PropertyTypes
    actual_price: float
    selling_price: float = 0.0
    features: dict = {}
    
    class Config:
        from_attributes = True



class PropertyListSchema(Schema):
    id: uuid.UUID
    name: str
    image: str
    description: str
    location: str
    status: Optional[StatusType] = None
    property_types: Optional[PropertyTypes] = None
    actual_price: float
    selling_price: float = 0.0
    features: dict = {}
    
    class Config:
        from_attributes = True


class PropertyListResponse(Schema):
    page: int
    count: int
    stats: Dict = {}
    items: List[PropertyListSchema]



class PropertySchema1(Schema):
    name: str = None
    image: str = None
    description: str = None
    location: str = None
    status: StatusType = None
    property_types: PropertyTypes = None
    actual_price: float = None
    selling_price: float = None
    features: dict = None
    
    class Config:
        from_attributes = True


class PropertyUpdateSerializer2(BaseModel):
    id: uuid.UUID
    data: PropertySchema1