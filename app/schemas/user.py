from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr | None = None
    is_active: bool | None = None


class ActivationTokenBase(BaseModel):
    token: str
    expiration_date: datetime
    user_id: int


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    activation_tokens: list[ActivationTokenBase]


class UserCreateReq(BaseModel):
    email: EmailStr
    password: str


class UserCreateRes(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr


class UserActivationReq(BaseModel):
    email: EmailStr


class UserActivationRes(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    is_active: bool


class ActivationToken(ActivationTokenBase):
    id: int
