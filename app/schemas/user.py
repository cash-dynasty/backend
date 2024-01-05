from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    email: str | None = None
    disabled: bool | None = None


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True
