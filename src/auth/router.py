from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.auth.schemas import RegisterUser
from src.auth.service import User

auth_router = APIRouter(prefix="/auth")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: RegisterUser):
    registered_user_id = User().register_user(user=user)
    return {"detail": f"User registered with ID {registered_user_id}"}


@auth_router.post("/token")
def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return form_data
