from pydantic import SecretStr

from .base import BaseClientModel

__all__ = ["User"]


class User(BaseClientModel):
    """Model for storage user data."""

    login: str
    password: SecretStr
