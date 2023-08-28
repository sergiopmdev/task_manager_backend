from unittest.mock import patch

import pytest

from src.auth.exceptions import UserBadCredentials
from src.auth.schemas import LoginUser
from src.auth.service import User


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
