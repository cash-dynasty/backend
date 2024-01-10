from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Relationship


class Company(Base):
    __tablename__ = "company"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True)
    owner = Relationship("User")
