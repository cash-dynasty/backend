from typing import Union

from pydantic import BaseModel, EmailStr


# ////////// AUTH //////////
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None


# ////////// USER //////////
class User(BaseModel):
    username: str
    email: str | None
    disabled: bool | None


class UserInDB(User):
    hashed_password: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True
