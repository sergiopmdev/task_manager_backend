import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from src.auth.exceptions import TokenError

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


class Auth:
    """
    Class in charge of handling the
    generation, verification
    and updating of tokens

    Attributes
    ----------
    _secret_key : str
        Key to use in the token generation
    _algorithm : str
        Algorithm to encode the data
    _expire_minutes : int
        Expiration minutes of the token

    Methods
    -------
    create_access_token()
        Create access token
    """

    def __init__(self):
        """
        Initialize Auth class
        """

        self._secret_key = os.getenv("SECRET_KEY")
        self._algorithm = "HS256"
        self._expire_minutes = 30

    def create_access_token(self) -> str:
        """
        Create access token

        Returns
        -------
        str
            Access token
        """

        return jwt.encode(
            {"exp": datetime.utcnow() + timedelta(minutes=self._expire_minutes)},
            self._secret_key,
            algorithm=self._algorithm,
        )

    def decode_token(self, token: str) -> None:
        """
        Decode token to check if it is valid

        Parameters
        ----------
        token : str
            Token to be decoded

        Raises
        ------
        TokenError
            Error occurring when a problem
            arises when decoding a token
        """

        try:
            jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
        except JWTError:
            raise TokenError("Invalid token")
