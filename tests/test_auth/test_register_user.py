from unittest.mock import Mock, patch

import pytest
from fastapi.testclient import TestClient

from src.auth.exceptions import UserAlreadyExists
from src.auth.schemas import RegisterUser
from src.auth.service import User
from src.main import app

test_client = TestClient(app)


@pytest.fixture
def mocked_user() -> RegisterUser:
    return RegisterUser(
        name="mocked_name",
        email="mocked_email",
        password="mocked_password",
    )


def test_register_user_properties():
    with patch("src.auth.service.Database.instantiate_client"):
        assert User()._db_client._extract_mock_name() == "instantiate_client()"


def test_register_user_already_exists(mocked_user: RegisterUser):
    with patch("src.auth.service.Database.instantiate_client"):
        with pytest.raises(UserAlreadyExists):
            user = User()
            mock_get_user = Mock()
            mock_get_user.return_value = {"found": True}
            user._get_user = mock_get_user
            user.register_user(mocked_user)


def test_register_user_succesfull(mocked_user: RegisterUser):
    with (
        patch("src.auth.service.Database.instantiate_client"),
        patch("src.auth.service.Utils.get_user") as mocked_get_user,
    ):
        user = User()
        mocked_get_user.return_value = None
        mocked_id = "mocked_id"
        user._users_collection.insert_one.return_value.inserted_id = mocked_id
        assert user.register_user(mocked_user) == mocked_id


def test_register_user_route_409(mocked_user: RegisterUser):
    with (
        patch("src.auth.service.Database.instantiate_client"),
        patch("src.auth.service.Utils.get_user") as mock_get_user,
    ):
        mock_get_user.return_value = {"found": True}
        response = test_client.post(
            "/auth/register",
            json={
                "name": mocked_user.name,
                "email": mocked_user.email,
                "password": mocked_user.password.get_secret_value(),
            },
        )
        assert response.status_code == 409
        assert response.json() == {"detail": "User already exists"}


def test_register_user_route_201(mocked_user: RegisterUser):
    with (
        patch("src.auth.service.Database.instantiate_client") as mock_db_client,
        patch("src.auth.service.Utils.get_user") as mock_get_user,
    ):
        mocked_id = "mocked_id"
        mock_db_client.return_value["users_db"][
            "users_collection"
        ].insert_one.return_value.inserted_id = mocked_id
        mock_get_user.return_value = None
        response = test_client.post(
            "/auth/register",
            json={
                "name": mocked_user.name,
                "email": mocked_user.email,
                "password": mocked_user.password.get_secret_value(),
            },
        )
        assert response.status_code == 201
        assert response.json() == {"detail": f"User registered with ID {mocked_id}"}
