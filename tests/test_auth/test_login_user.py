from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from src.auth.exceptions import UserBadCredentials
from src.auth.schemas import LoginUser
from src.auth.service import User
from src.main import app

test_client = TestClient(app)


@pytest.fixture
def mocked_user() -> LoginUser:
    return LoginUser(
        email="mocked_email",
        password="mocked_password",
    )


def test_login_user_does_not_exists(mocked_user: LoginUser):
    with (
        patch("src.auth.service.Database.instantiate_client"),
        patch("src.auth.service.Utils.get_user") as mocked_get_user,
    ):
        with pytest.raises(UserBadCredentials):
            user = User()
            mocked_get_user.return_value = {}
            user.login_user(mocked_user)


def test_login_user_wrong_password(mocked_user: LoginUser):
    with (
        patch("src.auth.service.Database.instantiate_client"),
        patch("src.auth.service.Utils.get_user") as mocked_get_user,
        patch("src.auth.service.pwd_context.verify") as mocked_verify,
    ):
        with pytest.raises(UserBadCredentials):
            user = User()
            mocked_get_user.return_value = {"password": "mocked_password"}
            mocked_verify.return_value = False
            user.login_user(mocked_user)


def test_login_user_route_401_user_does_not_exists(mocked_user: LoginUser):
    with (
        patch("src.auth.service.Database.instantiate_client"),
        patch("src.auth.service.Utils.get_user") as mock_get_user,
    ):
        mock_get_user.return_value = {}
        response = test_client.post(
            "/auth/token",
            data={"username": mocked_user.email, "password": mocked_user.password},
        )
        assert response.status_code == 401
        assert response.json() == {"detail": "Wrong credentials"}


def test_login_user_route_401_wrong_password(mocked_user: LoginUser):
    with (
        patch("src.auth.service.Database.instantiate_client"),
        patch("src.auth.service.Utils.get_user") as mock_get_user,
        patch("src.auth.service.pwd_context.verify") as mocked_verify,
    ):
        mock_get_user.return_value = {"password": "mocked_password"}
        mocked_verify.return_value = False
        response = test_client.post(
            "/auth/token",
            data={"username": mocked_user.email, "password": mocked_user.password},
        )
        assert response.status_code == 401
        assert response.json() == {"detail": "Wrong credentials"}


def test_login_user_route_200(mocked_user: LoginUser):
    with (
        patch("src.auth.service.Database.instantiate_client"),
        patch("src.auth.service.Utils.get_user") as mocked_get_user,
        patch("src.auth.service.pwd_context.verify") as mocked_verify,
        patch("src.auth.auth.Auth.create_access_token") as mocked_access_token,
    ):
        mocked_get_user.return_value = {
            "name": "mocked_name",
            "email": "mocked_email",
            "password": "mocked_password",
        }
        mocked_verify.return_value = True
        mocked_access_token.return_value = "mocked_token"
        response = test_client.post(
            "/auth/token",
            data={"username": mocked_user.email, "password": mocked_user.password},
        )
        assert response.status_code == 200
        assert response.json() == {
            "user_data": {"name": "mocked_name", "email": "mocked_email"},
            "access_token": "mocked_token",
            "token_type": "bearer",
        }
