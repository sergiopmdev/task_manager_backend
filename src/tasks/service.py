from typing import Any, Dict, List, Union

from src.auth.auth import Auth
from src.auth.exceptions import TokenError
from src.database.Database import Database
from src.tasks.exceptions import NotAuthorizedError, UserDoesNotExists
from src.utils import Utils


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

    def get_user_tasks(
        self, email: str, token: str
    ) -> List[Union[Any, Dict[str, Any]]]:
        """
        Obtain the tasks associated with a
        user by searching for him by email

        Parameters
        ----------
        email : str
            Email of the user
        token : str
            Bearer token

        Returns
        -------
        List[Union[Any, Dict[str, Any]]]
           Tasks associated with the user

        Raises
        ------
        NotAuthorizedError
            Error occurring when a request or an action
            could not be validated prior to being executed
        UserDoesNotExists
            Error occurring when a user
            is not found in the database
        """

        try:
            self._auth.decode_token(token=token)
        except TokenError:
            raise NotAuthorizedError(status_code=401, detail="Not authorized")

        user = Utils().get_user(user_email=email)

        if not user:
            raise UserDoesNotExists(status_code=404, detail="User not found in DB")

        return user["tasks"]
