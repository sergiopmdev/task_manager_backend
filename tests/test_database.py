import os
from unittest.mock import Mock, patch

import pytest

from src.database.Database import Database
from src.database.exceptions import ClientError, CredentialsNotFound, DatabaseError

MOCKED_ENV_VALUES = {"filled_value": "mocked_uri", "empty_value": str()}


@patch.dict(os.environ, {"MONGODB_URI": MOCKED_ENV_VALUES["filled_value"]})
def test_database_uri_value():
    assert Database()._MONGODB_URI == "mocked_uri"


@patch.dict(os.environ, {"MONGODB_URI": MOCKED_ENV_VALUES["empty_value"]})
def test_database_uri_not_found():
    with pytest.raises(CredentialsNotFound):
        Database().instantiate_client()


@patch.dict(os.environ, {"MONGODB_URI": MOCKED_ENV_VALUES["filled_value"]})
@patch("src.database.Database.MongoClient")
def test_database_client_error(mocked_mongo_client: Mock):
    mocked_mongo_client.side_effect = Exception()
    with pytest.raises(ClientError):
        Database().instantiate_client()


@patch.dict(os.environ, {"MONGODB_URI": MOCKED_ENV_VALUES["filled_value"]})
@patch("src.database.Database.MongoClient")
def test_database_database_error(mocked_mongo_client: Mock):
    mocked_mongo_client.return_value.admin.command.side_effect = Exception()
    with pytest.raises(DatabaseError):
        Database().instantiate_client()


@patch.dict(os.environ, {"MONGODB_URI": MOCKED_ENV_VALUES["filled_value"]})
def test_database_successful_connection():
    with patch("src.database.Database.MongoClient"):
        client = Database().instantiate_client()
    assert client._extract_mock_name() == "MongoClient()"
