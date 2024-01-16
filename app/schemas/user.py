from pydantic import BaseModel, ConfigDict, EmailStr


# TODO przemodelować wszystko


class User(BaseModel):
    username: str
    email: EmailStr | None = None
    is_active: bool | None = None


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr


class UserActivation(BaseModel):
    email: EmailStr
