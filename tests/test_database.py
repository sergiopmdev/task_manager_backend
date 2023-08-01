import os
from unittest.mock import Mock, patch

import pytest

from database import Database
from database.exceptions import ClientError, CredentialsNotFound, DatabaseError

MOCKED_URI_VALUES = {"filled": "mocked_uri", "empty": str()}


@patch.dict(os.environ, {"MONGODB_URI": MOCKED_URI_VALUES["filled"]})
def test_database_uri_value():
    assert Database()._MONGODB_URI == MOCKED_URI_VALUES["filled"]


@patch.dict(os.environ, {"MONGODB_URI": MOCKED_URI_VALUES["empty"]})
def test_database_uri_not_found():
    with pytest.raises(CredentialsNotFound):
        Database().instantiate_client()


@patch("database.Database.MongoClient")
def test_database_client_error(mocked_mongo_client: Mock):
    mocked_mongo_client.side_effect = Exception()
    with pytest.raises(ClientError):
        Database().instantiate_client()


@patch("database.Database.MongoClient")
def test_database_database_error(mocked_mongo_client: Mock):
    mocked_mongo_client.return_value.admin.command.side_effect = Exception()
    with pytest.raises(DatabaseError):
        Database().instantiate_client()


def test_database_successful_connection():
    with patch("database.Database.MongoClient"):
        client = Database().instantiate_client()
    assert client._extract_mock_name() == "MongoClient()"
