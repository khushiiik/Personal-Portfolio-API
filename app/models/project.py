from sqlalchemy import (Column, String, Boolean, Integer, Text, Date, ForeignKey)
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone

class Project(Base):
    __tablename__ = "projects"

    # Primary key field.
    id = Column(Integer,primary_key=True,index=True)

    name = Column(String(200), nullable=False)
    project_link = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    is_current = Column(Boolean, default=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    created_at = Column(Date, default=datetime.now(timezone.utc))
    updated_at = Column(Date, default=datetime.now(timezone.utc), updated_at = datetime.now(timezone.utc))

    # Foreign key field.
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship field.
    users = relationship("User", back_populates="projects")
