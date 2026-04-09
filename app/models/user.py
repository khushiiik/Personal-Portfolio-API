from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SAEnum
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone


# Restrict role to only "user" or "admin".
class UserRoll(str, enum.Enum):
    user = "user"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    # Primary key field.
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Handle user role.
    role = Column(SAEnum(UserRoll), default=UserRoll.user)

    # Relationship field.
    projects = relationship(
        "Project", back_populates="user", cascade="all, delete-orphan"
    )
    skills = relationship("Skill", secondary="users_skills", back_populates="users")
    experiences = relationship(
        "Experience", back_populates="user", cascade="all, delete-orphan"
    )
