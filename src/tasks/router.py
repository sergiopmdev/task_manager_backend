from fastapi import APIRouter, Depends, status

from src.auth.auth import oauth2_scheme
from src.tasks.schemas import Task
from src.tasks.service import Tasks

tasks_router = APIRouter(prefix="/tasks")


@tasks_router.post("/get_tasks", status_code=status.HTTP_200_OK)
def get_tasks(user_email: str, token: str = Depends(oauth2_scheme)):
    get_tasks_response = Tasks().get_user_tasks(email=user_email, token=token)
    return {"tasks": get_tasks_response}


@tasks_router.post("/add_task", status_code=status.HTTP_200_OK)
def add_task(user_email: str, task: Task, token: str = Depends(oauth2_scheme)):
    add_task_response = Tasks().add_task(email=user_email, new_task=task, token=token)
    return {"detail": add_task_response}
