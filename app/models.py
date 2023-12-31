from sqlalchemy import Column, Integer, String, Boolean
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    is_activee = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
