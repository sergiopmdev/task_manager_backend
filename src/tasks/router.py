from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.auth.auth import oauth2_scheme
from src.tasks.service import Tasks

tasks_router = APIRouter(prefix="/tasks")


@tasks_router.post("/get_tasks", status_code=status.HTTP_200_OK)
def get_tasks(user_email: str, token: str = Depends(oauth2_scheme)):
    get_tasks_response = Tasks().get_user_tasks(email=user_email, token=token)
    return {"response": get_tasks_response}
