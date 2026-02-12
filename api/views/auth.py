from random import shuffle
import uuid
from ninja import  Form, Router

from api.config.jwt_config import decode_jwt_token, generate_access_token, generate_refresh_token
from api.helpers.dbfunc import createBlackListedTokens
from api.lib.message import XResponse
from api.models.users import LoginTracker, User
from api.schema.usersSchema import LoginSerializer, SignupSerializer, UserSerializer, UserUpdateSerializer
from decouple import config
from ninja.errors import HttpError

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
                return  XResponse(status_code=400, data=None, message="Incorrect Password", status=False).response
            
            token = generate_access_token(user=user, secret_key=secret_key)
            refresh_token, jti = generate_refresh_token(user=user, secret_key=secret_key)    
            
            
            u = request.META
            AGENT = u.get("HTTP_USER_AGENT", "...")
            HTTP_SEC_CH_UA_PLATFORM = u.get("HTTP_SEC_CH_UA_PLATFORM", "...")
            REMOTE_ADDR = u.get("REMOTE_ADDR", "...")
            
            
            #track users login history
            lTracker = LoginTracker.objects.filter(
                user=user,
                agent=AGENT
            )
            
    
            LoginTracker.objects.update_or_create(
                    user=user,
                    agent=AGENT,
                    location=REMOTE_ADDR,
                    platform=HTTP_SEC_CH_UA_PLATFORM
                )
            return 200, {
                "access_token": token,
                "refresh_token": refresh_token,
                "jti": jti
            }
        else:
            return XResponse(status_code=400, data=None, message="Invalid credentials", status=False).response
    except Exception as e:
        # print(e)
        return XResponse(status_code=400, data=None, message="Error While Signing in", status=False).response



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
            return XResponse(status_code=400, data=None, message="Email already exists", status=False).response
        
        
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
        return XResponse(status_code=400, data=None, message="Email already exists", status=False).response
    
    
    
@router.post("/refresh_token", response={200: dict, 400: dict}, auth=None)
def refresh_token(request, refresh_token: str  ):
    try:
        secret_key = config('SECRET_KEY', default='django-insecure-f2^)s*hn*y_rix*@7vtk(srq_cbrkex@xr98!&+-+d9!!ft7+c')     
        token_decode = decode_jwt_token(refresh_token, secret_key=secret_key)
        
        if token_decode is None or token_decode.get("type") != "refresh":
            return XResponse(status_code=400, data=None, message="Invalid refresh token", status=False).response
        
        user_id = token_decode.get("sub")
        user = User.objects.filter(id=user_id)
        
        if not user.exists():
            return XResponse(status_code=400, data=None, message="User not found", status=False).response
        user = user.first()
        
        new_access_token = generate_access_token(user=user, secret_key=secret_key)
        return 200, {"access_token": new_access_token}
    
    except Exception as e:
        return XResponse(status_code=500, data=None, message="An error occurred", status=False).response



@router.get("/me", response={200: dict, 400: dict})
def get_user(request):

    try:
        user = request.auth    
        
        if user is None:
            return XResponse(status_code=400, data=None, message="User not authenticated", status=False).response
        
        
        user_object = User.objects.get(id=user.id)
        hist = user_object.login_histories()
        
        
        dt = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "phone_number":user_object.phone_number,
            'date_joined': user_object.date_joined,
            "login_histories": hist
            
        }
        
        user_data = UserSerializer.model_validate(dt).model_dump()
        return XResponse(status_code=200, data=user_data, message="Successful", status=True).response
    
    except Exception as e:
        return XResponse(status_code=400, data=None, message="Error occurred", status=False).response
    
    
    


@router.post("/signout", response={200: dict, 400: dict})
def signout_user(request):
    try:
        user = request.auth
        token = request.META.get("HTTP_AUTHORIZATION", None).split("Bearer")[1]
        
        if user is None:
            return XResponse(status_code=400, data=None, message="User not authenticated", status=False).response
        
        createBlackListedTokens(token=token.lstrip(" "))
        return XResponse(status_code=200, data=None, message="Successful logged out.", status=True).response
    
    except Exception as e:
        return XResponse(status_code=400, data=None, message="Error occurred", status=False).response
    
    




@router.put("/updateSignedUser", response={200: dict, 400: dict, 401: dict})
def auth_update_signed_user(request, data: UserUpdateSerializer):
    
    if not request.auth:
        raise HttpError(401, "Unauthorized")

    try:
        user = User.objects.get(id=request.auth.id)

        # remove None values only
        payload = {
            k: v for k, v in data.model_dump().items()
            if v is not None
        }

        for attr, value in payload.items():
            setattr(user, attr, value)

        user.save()

        user_data = UserSerializer.model_validate(user).model_dump(exclude={"login_histories", "date_joined", "id", "email","role","username"})
        # print(user_data)
        return XResponse(
            status_code=200,
            data=user_data,
            message="User updated successfully",
            status=True,
        ).response

    except User.DoesNotExist:
        return XResponse(
            status_code=400,
            data=None,
            message="User not found",
            status=False,
        ).response

    except Exception as e:
        # print("Update user error:", e)
        return XResponse(
            status_code=400,
            data=None,
            message="An error occurred while updating user",
            status=False,
        ).response