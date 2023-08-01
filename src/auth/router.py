from fastapi import APIRouter, status

from auth.schemas import RegisterUser
from auth.service import User

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: RegisterUser):
    registered_user_id = User().register_user(user=user)
    return {"detail": f"User registered with ID {registered_user_id}"}
