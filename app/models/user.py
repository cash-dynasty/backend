from database import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=False)


class ActivationToken(Base):
    __tablename__ = "activation_tokens"

    id = Column(Integer, primary_key=True)
    token = Column(String)
    expiration_date = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
