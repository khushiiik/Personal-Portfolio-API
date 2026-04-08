from sqlalchemy import (Column, Integer, String, ForeignKey, Boolean, UniqueConstraint)
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone
from . import project_skills

class Skill(Base):
    __tablename__ = "skills"

    # Primary key field.
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    # Foreign key field.
    user_id = Column("User", ForeignKey("users.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("name", "user_id", name="unique_user_skill"),
    )

    # Relationship field
    user = relationship("User", back_populates="skills")
    projects = relationship("Project", secondary=project_skills, back_populates="skills")