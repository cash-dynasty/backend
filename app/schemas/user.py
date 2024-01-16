from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: str | None = None
    is_active: bool
    player_name: str | None = None

    model_config = ConfigDict(from_attributes=True)


class User(UserBase):
    id: int
    password: str


class UserCreateReq(BaseModel):
    email: EmailStr
    password: str


class UserCreateRes(UserBase):
    id: int
