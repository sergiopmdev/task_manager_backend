from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from src.auth.exceptions import TokenError
from src.main import app
from src.tasks.exceptions import NotAuthorizedError, UserDoesNotExists
from src.tasks.service import Tasks

test_client = TestClient(app)

MOCKED_EMAIL = "mocked_email"
MOCKED_TOKEN = "mocked_token"


def test_get_user_tasks_invalid_token():
    with (
        patch("src.tasks.service.Database.instantiate_client"),
        patch("src.auth.auth.Auth.decode_token") as mocked_decode_token,
    ):
        mocked_decode_token.side_effect = TokenError
        with pytest.raises(NotAuthorizedError):
            Tasks().get_user_tasks(email=MOCKED_EMAIL, token=MOCKED_TOKEN)


def test_get_user_tasks_user_does_not_exists():
    with (
        patch("src.tasks.service.Database.instantiate_client"),
        patch("src.auth.auth.Auth.decode_token"),
        patch("src.auth.service.Utils.get_user") as mock_get_user,
    ):
        mock_get_user.return_value = {}
        with pytest.raises(UserDoesNotExists):
            Tasks().get_user_tasks(email=MOCKED_EMAIL, token=MOCKED_TOKEN)


def test_get_user_tasks_route_401():
    with (
        patch("src.auth.service.Database.instantiate_client"),
        patch("src.auth.auth.Auth.decode_token") as mocked_decode_token,
    ):
        mocked_decode_token.side_effect = TokenError
        response = test_client.post(
            f"/tasks/get_tasks?user_email={MOCKED_EMAIL}",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {MOCKED_TOKEN}",
            },
        )
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authorized"}


def test_get_user_tasks_route_404():
    with (
        patch("src.auth.service.Database.instantiate_client"),
        patch("src.auth.auth.Auth.decode_token"),
        patch("src.auth.service.Utils.get_user") as mock_get_user,
    ):
        mock_get_user.return_value = {}
        response = test_client.post(
            f"/tasks/get_tasks?user_email={MOCKED_EMAIL}",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {MOCKED_TOKEN}",
            },
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found in DB"}


def test_get_user_tasks_route_200():
    with (
        patch("src.auth.service.Database.instantiate_client"),
        patch("src.auth.auth.Auth.decode_token"),
        patch("src.auth.service.Utils.get_user") as mock_get_user,
    ):
        mock_get_user.return_value = {"tasks": {}}
        response = test_client.post(
            f"/tasks/get_tasks?user_email={MOCKED_EMAIL}",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {MOCKED_TOKEN}",
            },
        )
        assert response.status_code == 200
        assert response.json() == {"tasks": {}}
