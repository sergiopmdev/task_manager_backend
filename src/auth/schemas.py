from typing import Any, List

from pydantic import BaseModel, SecretStr


class RegisterUser(BaseModel):
    name: str
    email: str
    password: SecretStr
    tasks: List[Any] = []
