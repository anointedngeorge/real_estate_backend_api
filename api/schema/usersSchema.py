from datetime import date, datetime
from typing import Any, List, Optional, Union
import uuid
from ninja import Schema, Field
from pydantic import BaseModel
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
    login_histories: List | str

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
    permissions: List
    

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