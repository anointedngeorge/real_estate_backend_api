from ninja import NinjaAPI, Router
# Import and include your app-specific routers here
from api.config.jwt_config import decode_jwt_token
from api.lib.message import XResponse

from api.views.n8n_views.realtors import router as realtors_router
from api.views.n8n_views.clients import router as client_router
from api.views.n8n_views.properties import router as property_router

from ninja.errors import ValidationError, AuthenticationError
from ninja.responses import Response
from ninja.security import HttpBearer
from decouple import config
from api.models.users import User, BlackListedTokens




class GlobalAuthentication(HttpBearer):
    
    # Override the authenticate method to decode the JWT token and retrieve the user
    def authenticate(self, request, token):
        try:
            secret_key = config('SECRET_KEY', default='django-insecure-f2^)s*hn*y_rix*@7vtk(srq_cbrkex@xr98!&+-+d9!!ft7+c')
            token_decode = decode_jwt_token(token, secret_key=secret_key)
        
            if token_decode is None:
                return None
 
            if BlackListedTokens.objects.filter(token=token).exists():
                return None
            
            user_id = token_decode.get("sub")
            user = User.objects.filter(id=user_id, email=token_decode.get("email"))
            
            if not user.exists():
                return None
            
            return user.first()
        except Exception as e:
            # print("failed to authenticate user...", e)
            return None



n8n_api = NinjaAPI(
    auth=None,
    title="Real Estate Backend API For N8N",
    description="API for Backend Application for connecting with n8n",
    version="1.0.0",
    urls_namespace="n8n"
)



@n8n_api.exception_handler(ValidationError)
def validation_handler(request, exc):
    # print(exc.errors[0].get("msg", ""), "error")
    # import traceback
    # traceback.print_exc()
    return Response(
        {"errors": exc.errors[0].get("loc", []), "message": exc.errors[0].get("msg", "")},
        status=422
    )
    

@n8n_api.exception_handler(Exception)
def global_handler(request, exc):
    import traceback
    traceback.print_exc()
    return Response(
        {"detail": "Internal server error"},
        status=500
    )
    


@n8n_api.exception_handler(AuthenticationError)
def global_handler_authorization(request, exc):
    return XResponse(status_code=401, data=None, message="Unauthorized", status=False).response



n8n_api.add_router(router=realtors_router, prefix="/realtors")
n8n_api.add_router(router=client_router, prefix="/client")
n8n_api.add_router(router=property_router, prefix="/properties")
