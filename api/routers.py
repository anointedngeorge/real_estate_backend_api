from ninja import NinjaAPI, Router
# Import and include your app-specific routers here
from api.config.jwt_config import decode_jwt_token
from api.views.users import router as users_router
from api.views.auth import router as auth_router
from ninja.errors import ValidationError
from ninja.responses import Response
from ninja.security import HttpBearer
from decouple import config
from api.models.users import User, BlackListedTokens




class GlobalAuthentication(HttpBearer):
    
    # Override the authenticate method to decode the JWT token and retrieve the user
    def authenticate(self, request, token):
        secret_key = config('SECRET_KEY', default='django-insecure-f2^)s*hn*y_rix*@7vtk(srq_cbrkex@xr98!&+-+d9!!ft7+c')
        token_decode = decode_jwt_token(token, secret_key=secret_key)
        
        if BlackListedTokens.objects.filter(jti=token_decode.get("jti"), token=token).exists():
            return None
        
        if token_decode is None:
            return None

        
        user_id = token_decode.get("sub")
        user = User.objects.filter(id=user_id, email=token_decode.get("email"))
        
        if not user.exists():
            return None
        
        return user.first()



api = NinjaAPI(
    auth=GlobalAuthentication(),
    title="Real Estate Backend API",
    description="API for Backend Application",
    version="1.0.0",
)



@api.exception_handler(ValidationError)
def validation_handler(request, exc):
    return Response(
        {"errors": exc.errors[0].get("loc", []), "message": exc.errors[0].get("msg", "")},
        status=422
    )
    

@api.exception_handler(Exception)
def global_handler(request, exc):
    return Response(
        {"detail": "Internal server error"},
        status=500
    )



api.add_router(router=auth_router, prefix="/auth")
api.add_router(router=users_router, prefix="/users")
