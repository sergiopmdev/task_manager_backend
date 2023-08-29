from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.schemas import LoginUser, RegisterUser
from src.auth.service import User

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: RegisterUser):
    registered_user_id = User().register_user(user=user)
    return {"detail": f"User registered with ID {registered_user_id}"}


@auth_router.post("/token", status_code=status.HTTP_200_OK)
def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_credentials = LoginUser(email=form_data.username, password=form_data.password)
    login_response = User().login_user(user=user_credentials)
    return {
        "user_data": login_response["user_data"],
        "access_token": login_response["token"],
        "token_type": "bearer",
    }
