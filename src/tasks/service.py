from typing import Any, Dict, List, Union

from src.auth.auth import Auth
from src.auth.exceptions import TokenError
from src.database.Database import Database
from src.tasks.exceptions import (
    NotAuthorizedError,
    TaskAlreadyExists,
    TaskDoesNotExist,
    UserDoesNotExists,
)
from src.tasks.schemas import Task
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
    get_user_tasks()
        Obtain the tasks associated with a
        user by searching for him by email
    add_task()
        Add new task to a user's task list
    delete_task()
        Delete task from user's task list
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

    def add_task(self, email: str, new_task: Task, token: str) -> str:
        """
        Add new task to a user's task list

        Parameters
        ----------
        email : str
            Email of the user
        new_task : Task
            New task to be added
        token : str
            Bearer token

        Returns
        -------
        str
            ID of the updated user

        Raises
        ------
        NotAuthorizedError
            Error occurring when a request or an action
            could not be validated prior to being executed
        TaskAlreadyExists
            Error occurring when the new task that
            is trying to be inserted already exists
        """

        try:
            self._auth.decode_token(token=token)
        except TokenError:
            raise NotAuthorizedError(status_code=401, detail="Not authorized")

        user = Utils().get_user(user_email=email)

        user_id = user["_id"]
        tasks = user["tasks"]

        new_task_dict = new_task.model_dump()

        for task in tasks:
            if task["name"] == new_task_dict["name"]:
                raise TaskAlreadyExists(status_code=409, detail="Task already exists")

        tasks.append(new_task_dict)

        self._users_collection.update_one({"email": email}, {"$set": {"tasks": tasks}})

        return f"Tasks updated for the user with ID {user_id}"

    def delete_task(self, email: str, task_name: str, token: str) -> str:
        """
        Delete task from user's task list

        Parameters
        ----------
        email : str
            Email of the user
        task_name : str
            Task to be deleted
        token : str
            Bearer token

        Returns
        -------
        str
            ID of the updated user
        """

        try:
            self._auth.decode_token(token=token)
        except TokenError:
            raise NotAuthorizedError(status_code=401, detail="Not authorized")

        user = Utils().get_user(user_email=email)

        user_id = user["_id"]
        tasks = user["tasks"]

        updated_tasks = []

        for task in tasks:
            if not task["name"] == task_name:
                updated_tasks.append(task)

        if tasks == updated_tasks:
            raise TaskDoesNotExist(status_code=404, detail="Task does not exist")

        self._users_collection.update_one(
            {"email": email}, {"$set": {"tasks": updated_tasks}}
        )

        return f"Tasks updated for the user with ID {user_id}"
