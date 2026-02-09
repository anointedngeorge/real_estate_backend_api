from random import shuffle
import uuid
from ninja import  Form, Router

from api.config.jwt_config import decode_jwt_token, generate_access_token, generate_refresh_token
from api.lib.message import XResponse
from api.models.users import User
from api.schema.usersSchema import LoginSerializer, SignupSerializer, UserSerializer
from decouple import config


router = Router(tags=["Authentication"])





@router.post("/signin", response={200: dict, 400: dict}, auth=None)
def auth_signin(request, data: LoginSerializer ):
    try:
        username = data.username
        password = data.password
        
        secret_key = config('SECRET_KEY', default='django-insecure-f2^)s*hn*y_rix*@7vtk(srq_cbrkex@xr98!&+-+d9!!ft7+c')
        
        user = User.objects.filter(email=username)
                
        if user.exists():
            user = user.first()
            
            if not user.check_password(password):
                return 400, {"result": "Invalid Password"}
            
            token = generate_access_token(user=user, secret_key=secret_key)
            refresh_token, jti = generate_refresh_token(user=user, secret_key=secret_key)    
            
            return 200, {
                "access_token": token,
                "refresh_token": refresh_token,
                "jti": jti
            }
        else:
            return 400, {"result": "Invalid credentials"}
    except Exception as e:
        # print("Error during signin:", str(e))
        return 400, {"result": str(e)}



def username(first_name, last_name):
    st = str(first_name) + str(last_name).lower()
    st_list = list(st)
    shuffle(st_list)
    return ''.join(st_list)[:4] + str(uuid.uuid4())[:8]



@router.post("/signup", auth=None, response={200: dict, 400: dict})
def auth_signup(request, data: SignupSerializer):
    try:

        user = User.objects 
        if user.filter(email=data.email).exists():
            return 400, {"result": "Email already exists"}
        
        
        username_generated = username(data.first_name, data.last_name)  
        
        data_dict = data.model_dump()
        password =  data_dict.pop("password")

        data_dict["username"] = username_generated
        
        
        user_created = user.create(**data_dict)
        user_created.is_active = True
        user_created.is_staff = True
        user_created.set_password(password)
        user_created.save()
        
        return 200, {"result": f"User {user_created.username} created successfully"}
    
    except Exception as e:
        return 400, {"result": str(e)}
    
    
    


@router.post("/refresh_token", response={200: dict, 400: dict}, auth=None)
def refresh_token(request, refresh_token: str  ):
    try:
        secret_key = config('SECRET_KEY', default='django-insecure-f2^)s*hn*y_rix*@7vtk(srq_cbrkex@xr98!&+-+d9!!ft7+c')     
        token_decode = decode_jwt_token(refresh_token, secret_key=secret_key)
        
        if token_decode is None or token_decode.get("type") != "refresh":
            return 400, {"result": "Invalid refresh token"} 
        
        user_id = token_decode.get("sub")
        user = User.objects.filter(id=user_id)
        
        if not user.exists():
            return 400, {"result": "User not found"}
        user = user.first()
        
        new_access_token = generate_access_token(user=user, secret_key=secret_key)
        return 200, {"access_token": new_access_token}
    
    except Exception as e:
        return 400, {"result": str(e)}
    



@router.get("/me", response={200: dict, 400: dict})
def get_user(request):

    try:
        user = request.auth    
            
        if user is None:
            return XResponse(status_code=400, data=None, message="User not authenticated", status=False).response
        
        dt = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role
        }
        user_data = UserSerializer.model_validate(dt).model_dump()
        return XResponse(status_code=200, data=user_data, message="Successful", status=True).response
    
    except Exception as e:
        return XResponse(status_code=400, data=None, message="Error occurred", status=False).response