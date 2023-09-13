from fastapi import HTTPException


class NotAuthorizedError(HTTPException):
    """
    Error occurring when a request or an action
    could not be validated prior to being executed
    """

    pass


class UserDoesNotExists(HTTPException):
    """
    Error occurring when a user
    is not found in the database
    """

    pass


class TaskAlreadyExists(HTTPException):
    """
    Error occurring when the new task that
    is trying to be inserted already exists
    """


class TaskDoesNotExist(HTTPException):
    """
    Error occurring when the task you
    are trying to delete does not exist
    """
