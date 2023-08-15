from typing import Any, Dict, Optional

from fastapi import HTTPException

from src.auth.auth import Auth
from src.auth.exceptions import TokenError
from src.database.Database import Database


class Tasks:
    """
    Class in charge of handling all
    the actions related to
    the tasks of a user

    Attributes
    ----------
    _db_client : pymongo.MongoClient
        MongoDB client
    _users_collection : pymongo.collection.Collection
        Users collection
    _auth : Auth
        Authentication handler

    Methods
    -------
    _get_user()
        Get an user from the users collection
    """

    def __init__(self) -> None:
        """
        Initialize User class
        """

        self._db_client = Database().instantiate_client()
        self._users_collection = self._db_client["users_db"]["users_collection"]
        self._auth = Auth()

    def get_user_tasks(self, email: str, token: str) -> Any:
        ...

        try:
            self._auth.decode_token(token=token)
        except TokenError:
            raise HTTPException(status_code=401, detail="Not authorized")

        return email

    def _get_user(self, user_email: str) -> Optional[Dict[str, Any]]:
        """
        Get an user from the users collection

        Parameters
        ----------
        user_email : str
            Email of the user

        Returns
        -------
        Optional[Dict[str, Any]]
            Data of the user if exists
        """

        return self._users_collection.find_one({"email": user_email})
