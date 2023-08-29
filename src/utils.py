from typing import Any, Dict, Optional

from src.database.Database import Database


class Utils:
    """
    Class in charge of handling all
    the utils used by the modules

    Attributes
    ----------
    _db_client : pymongo.MongoClient
        MongoDB client
    _users_collection : pymongo.collection.Collection
        Users collection

    Methods
    -------
    get_user()
        Get an user from the users collection
    """

    def __init__(self) -> None:
        """
        Initialize Utils class
        """

        self._db_client = Database().instantiate_client()
        self._users_collection = self._db_client["users_db"]["users_collection"]

    def get_user(self, user_email: str) -> Optional[Dict[str, Any]]:
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
