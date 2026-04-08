from sqlalchemy import (Column, Integer, String, Boolean)
from sqlalchemy.orm import relationship
from app.database import Base

# # Restrict role to only "user" or "admin".
# class UserRoll(str, enum.Enum):
#     user = "user"
#     admin = "admin"

class User(Base):
    __tablename__ = "users"

    # Primary key field.
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)
    email = Column(String(100),unique=True,index=True,nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean,default=True)

    # Relationship field.
    projects = relationship("Project", back_populates="user", cascade="all, delete")
    skills = relationship("Skill", back_populates="user", cascade="all, delete-orphan")