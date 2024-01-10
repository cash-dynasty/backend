from pydantic import BaseModel, ConfigDict, EmailStr


class User(BaseModel):
    username: str
    email: str | None = None
    disabled: bool | None = None
    player_name: str | None = None


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
