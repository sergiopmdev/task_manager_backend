from fastapi import HTTPException


class UserAlreadyExists(HTTPException):
    """
    Error occurring when registering
    an user that already exists
    """

    pass


class UserBadCredentials(HTTPException):
    """
    Error occurring when user
    credentials are not correct
    """

    pass


class TokenError(Exception):
    """
    Error occurring when a problem
    arises when decoding a token
    """
