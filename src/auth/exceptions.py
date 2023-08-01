from fastapi import HTTPException


class UserAlreadyExists(HTTPException):
    """
    Error occurring when registering
    an user that already exists
    """

    pass
