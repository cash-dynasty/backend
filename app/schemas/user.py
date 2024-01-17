from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


# TODO przemodelować wszystko


class UserBase(BaseModel):
    username: str
    email: EmailStr | None = None
    is_active: bool | None = None


class ActivationTokenBase(BaseModel):
    token: str
    expiration_date: datetime
    user_id: int


class User(UserBase):
    id: int
    activation_tokens: list[ActivationTokenBase]

    class Config:
        orm_mode = True


class UserCreateReq(BaseModel):
    email: EmailStr
    password: str


class UserCreateRes(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr


class UserActivationReq(BaseModel):
    email: EmailStr


class ActivationToken(ActivationTokenBase):
    id: int
