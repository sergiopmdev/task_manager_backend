from typing import Any, Dict, Optional

from bson.objectid import ObjectId
from passlib.context import CryptContext

from src.auth.auth import Auth
from src.auth.exceptions import UserAlreadyExists, UserBadCredentials
from src.auth.schemas import LoginUser, RegisterUser
from src.database.Database import Database

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User:
    """
    Class in charge of handling
    the user authentication

    Attributes
    ----------
    _db_client : pymongo.MongoClient
        MongoDB client
    _users_collection : pymongo.collection.Collection
        Users collection

    Methods
    -------
    register_user()
        Add a new user to the users collection
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

    def register_user(self, user: RegisterUser) -> ObjectId:
        """
        Add a new user to the users collection

        Parameters
        ----------
        user : RegisterUser
            User to be registered

        Returns
        -------
        ObjectId
            Document ID of the registered user

        Raises
        ------
        UserAlreadyExists
            Error when the user to be registered
            already exists in the users collection
        """

        user_email = user.email
        user_password = pwd_context.hash(user.password.get_secret_value())

        if self._get_user(user_email=user_email):
            raise UserAlreadyExists(status_code=409, detail="User already exists")

        registered_user_id = self._users_collection.insert_one(
            {
                "name": user.name,
                "email": user_email,
                "password": user_password,
                "tasks": user.tasks,
            }
        ).inserted_id

        self._db_client.close()

        return registered_user_id

    def login_user(self, user: LoginUser) -> Dict[str, str]:
        """
        Log the user in using the email and
        password and return the user's
        main data and a bearer token

        Parameters
        ----------
        user : LoginUser
            Email and password of the user

        Returns
        -------
        Dict[str, str]
            User's main data and a bearer token
        """

        LOGIN_ERROR_CODE = 401
        LOGIN_ERROR_MSG = "Wrong credentials"
        LOGIN_ERROR_HEADERS = {"WWW-Authenticate": "Bearer"}

        user_email = user.email
        user_password = user.password.get_secret_value()

        user = self._get_user(user_email=user_email)

        if not user:
            raise UserBadCredentials(
                status_code=LOGIN_ERROR_CODE,
                detail=LOGIN_ERROR_MSG,
                headers=LOGIN_ERROR_HEADERS,
            )

        if not pwd_context.verify(user_password, user["password"]):
            raise UserBadCredentials(
                status_code=LOGIN_ERROR_CODE,
                detail=LOGIN_ERROR_MSG,
                headers=LOGIN_ERROR_HEADERS,
            )

        data = {
            "user_data": {
                "name": user["name"],
                "email": user["email"],
            },
            "token": self._auth.create_access_token(),
        }

        return data

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
