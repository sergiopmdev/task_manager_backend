from fastapi import APIRouter, Depends, status

from src.auth.auth import oauth2_scheme
from src.tasks.schemas import Task
from src.tasks.service import Tasks

tasks_router = APIRouter(prefix="/tasks")


@tasks_router.post("/get_tasks", status_code=status.HTTP_200_OK)
def get_tasks(user_email: str, token: str = Depends(oauth2_scheme)):
    get_tasks_response = Tasks().get_user_tasks(email=user_email, token=token)
    return {"tasks": get_tasks_response}


@tasks_router.patch("/add_task", status_code=status.HTTP_200_OK)
def add_task(user_email: str, task: Task, token: str = Depends(oauth2_scheme)):
    add_task_response = Tasks().add_task(email=user_email, new_task=task, token=token)
    return {"detail": add_task_response}


@tasks_router.patch("/delete_task", status_code=status.HTTP_200_OK)
def delete_task(user_email: str, task_name: str, token: str = Depends(oauth2_scheme)):
    delete_task_response = Tasks().delete_task(
        email=user_email, task_name=task_name, token=token
    )
    return {"detail": delete_task_response}
