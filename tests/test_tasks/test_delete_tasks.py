from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.tasks.exceptions import TaskDoesNotExist
from src.tasks.service import Tasks

MOCKED_EMAIL = "mocked_email"
MOCKED_TOKEN = "mocked_token"
MOCKED_TASK_NAME = "mocked_task_name"


test_client = TestClient(app)


def test_delete_task_does_not_exist():
    with (
        patch("src.tasks.service.Database.instantiate_client"),
        patch("src.auth.auth.Auth.decode_token"),
        patch("src.auth.service.Utils.get_user") as mock_get_user,
    ):
        mock_get_user.return_value = {
            "_id": "mocked_id",
            "tasks": [{"name": "Different mocked task"}],
        }
        with pytest.raises(TaskDoesNotExist):
            Tasks().delete_task(
                email=MOCKED_EMAIL, task_name=MOCKED_TASK_NAME, token=MOCKED_TOKEN
            )


def test_delete_task_update_called():
    with (
        patch("src.tasks.service.Database.instantiate_client"),
        patch("src.auth.auth.Auth.decode_token"),
        patch("src.auth.service.Utils.get_user") as mock_get_user,
    ):
        tasks = Tasks()
        mock_get_user.return_value = {
            "_id": "mocked_id",
            "tasks": [{"name": MOCKED_TASK_NAME}],
        }

        tasks.delete_task(
            email=MOCKED_EMAIL, task_name=MOCKED_TASK_NAME, token=MOCKED_TOKEN
        )

        assert tasks._users_collection.update_one.called


def test_delete_task_route_404():
    with (
        patch("src.auth.service.Database.instantiate_client"),
        patch("src.auth.auth.Auth.decode_token"),
        patch("src.auth.service.Utils.get_user") as mock_get_user,
    ):
        mock_get_user.return_value = {
            "_id": "mocked_id",
            "tasks": [{"name": "Different mocked task"}],
        }
        response = test_client.patch(
            f"/tasks/delete_task?user_email={MOCKED_EMAIL}&task_name={MOCKED_TASK_NAME}",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {MOCKED_TOKEN}",
            },
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Task does not exist"}


def test_delete_task_route_200():
    with (
        patch("src.auth.service.Database.instantiate_client"),
        patch("src.auth.auth.Auth.decode_token"),
        patch("src.auth.service.Utils.get_user") as mock_get_user,
    ):
        mocked_id = "mocked_id"
        mock_get_user.return_value = {
            "_id": mocked_id,
            "tasks": [{"name": MOCKED_TASK_NAME}],
        }
        response = test_client.patch(
            f"/tasks/delete_task?user_email={MOCKED_EMAIL}&task_name={MOCKED_TASK_NAME}",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {MOCKED_TOKEN}",
            },
        )
        assert response.status_code == 200
        assert response.json() == {
            "detail": f"Tasks updated for the user with ID {mocked_id}"
        }
