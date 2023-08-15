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
