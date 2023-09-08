from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.tasks.exceptions import TaskAlreadyExists
from src.tasks.schemas import Task
from src.tasks.service import Tasks

test_client = TestClient(app)

MOCKED_EMAIL = "mocked_email"
MOCKED_TOKEN = "mocked_token"


@pytest.fixture
def task() -> Task:
    return Task(
        name="Mocked task",
        description="Description of the mocked task",
        priority="Low",
    )


def test_add_task_already_exists(task: Task):
    with (
        patch("src.tasks.service.Database.instantiate_client"),
        patch("src.auth.auth.Auth.decode_token"),
        patch("src.auth.service.Utils.get_user") as mock_get_user,
    ):
        mock_get_user.return_value = {
            "_id": "mocked_id",
            "tasks": [{"name": "Mocked task"}],
        }
        with pytest.raises(TaskAlreadyExists):
            Tasks().add_task(email=MOCKED_EMAIL, new_task=task, token=MOCKED_TOKEN)


def test_add_task_update_called(task: Task):
    with (
        patch("src.tasks.service.Database.instantiate_client"),
        patch("src.auth.auth.Auth.decode_token"),
        patch("src.auth.service.Utils.get_user") as mock_get_user,
    ):
        tasks = Tasks()
        mock_get_user.return_value = {
            "_id": "mocked_id",
            "tasks": [{"name": "Different mocked task"}],
        }
        Tasks().add_task(email=MOCKED_EMAIL, new_task=task, token=MOCKED_TOKEN)
        assert tasks._users_collection.update_one.called


def test_add_task_route_409(task: Task):
    with (
        patch("src.auth.service.Database.instantiate_client"),
        patch("src.auth.auth.Auth.decode_token"),
        patch("src.auth.service.Utils.get_user") as mock_get_user,
    ):
        mock_get_user.return_value = {
            "_id": "mocked_id",
            "tasks": [{"name": "Mocked task"}],
        }
        response = test_client.patch(
            f"/tasks/add_task?user_email={MOCKED_EMAIL}",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {MOCKED_TOKEN}",
            },
            json=task.model_dump(),
        )
        assert response.status_code == 409
        assert response.json() == {"detail": "Task already exists"}


def test_add_task_route_200(task: Task):
    with (
        patch("src.auth.service.Database.instantiate_client"),
        patch("src.auth.auth.Auth.decode_token"),
        patch("src.auth.service.Utils.get_user") as mock_get_user,
    ):
        mocked_id = "mocked_id"
        mock_get_user.return_value = {
            "_id": mocked_id,
            "tasks": [{"name": "Different mocked task"}],
        }
        response = test_client.patch(
            f"/tasks/add_task?user_email={MOCKED_EMAIL}",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {MOCKED_TOKEN}",
            },
            json=task.model_dump(),
        )
        assert response.status_code == 200
        assert response.json() == {
            "detail": f"Tasks updated for the user with ID {mocked_id}"
        }
