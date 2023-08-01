from fastapi import APIRouter

from auth.schemas import RegisterUser

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/register")
def register_user(user: RegisterUser):
    return user
