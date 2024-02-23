from database import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=False)

    activation_tokens = relationship("ActivationToken", backref="user")
    permissions = relationship("UserPermission", backref="user")


class ActivationToken(Base):
    __tablename__ = "activation_token"

    id = Column(Integer, primary_key=True)
    token = Column(String)
    expiration_date = Column(DateTime)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)


class UserPermission(Base):
    __tablename__ = "user_permission"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
