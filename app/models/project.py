from sqlalchemy import Column, String, Boolean,Date, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone
from . import project_skills


class Project(Base):
    __tablename__ = "projects"

    # Primary key field.
    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(200), nullable=False)
    project_link = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    is_current = Column(Boolean, default=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    is_archived = Column(Boolean, default=False)

    # Foreign key field.
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship field.
    user = relationship("User", back_populates="projects")
    skills = relationship("Skill", secondary=project_skills, back_populates="projects")
