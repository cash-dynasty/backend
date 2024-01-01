from typing import Union

from pydantic import BaseModel


# ////////// AUTH //////////
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


# ////////// USER //////////
class User(BaseModel):
    username: str
    email: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str
