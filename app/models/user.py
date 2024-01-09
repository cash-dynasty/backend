from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import declarative_base


UserBase = declarative_base()


class User(UserBase):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=False)
