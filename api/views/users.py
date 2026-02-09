from django.contrib import admin
from django.urls import path
from ninja import  Router



router = Router(tags=["users"])



@router.get("/users")
def users(request):
    user = request.auth
    
    print("Authenticated user:", user)
    return {"result": "This is the users endpoint"}