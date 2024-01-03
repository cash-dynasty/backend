from pydantic import BaseModel, EmailStr


# ////////// AUTH //////////
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


# ////////// USER //////////
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
