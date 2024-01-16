from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: str | None = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class User(UserBase):
    id: int
    password: str


class UserCreateReq(BaseModel):
    email: EmailStr
    password: str


class UserCreateRes(UserBase):
    id: int
