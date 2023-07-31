import os

from dotenv import load_dotenv
from pymongo import MongoClient

from database.exceptions import ClientError, CredentialsNotFound, DatabaseError

load_dotenv()


class Database:
    """
    Class in charge of handling
    the connection to the database

    Attributes
    ----------
    _MONGODB_URI : str
        Database connection string

    Methods
    -------
    instantiate_client()
        Instantiate MongoDB client
    """

    def __init__(self):
        self._MONGODB_URI = os.getenv("MONGODB_URI")

    def instantiate_client(self) -> MongoClient:
        """
        Instantiate MongoDB client

        Returns
        -------
        MongoClient
            MongoDB client

        Raises
        ------
        CredentialsNotFound
            MongoDB URI not found in the .env file
        ClientError
            Error instantiating the client
        DatabaseError
            Error when connecting to MongoDB database
        """

        if not self._MONGODB_URI:
            raise CredentialsNotFound("MongoDB URI not found in .env")

        try:
            client = MongoClient(self._MONGODB_URI)
        except Exception:
            raise ClientError("An error occurred instantiating the MongoDB client")

        try:
            client.admin.command("ping")
        except Exception:
            raise DatabaseError("An error occurred in the database connection")

        return client
