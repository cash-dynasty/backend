from sqlalchemy import Boolean, Column, Integer, String

from app.database import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=False)
    player_name = Column(String, unique=True, index=True, default="", nullable=True)
