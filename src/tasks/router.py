from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.auth.auth import oauth2_scheme

tasks_router = APIRouter(prefix="/tasks")


@tasks_router.post("/get_tasks", status_code=status.HTTP_200_OK)
def get_tasks(user_email: str, token: str = Depends(oauth2_scheme)):
    return {"email": user_email}
