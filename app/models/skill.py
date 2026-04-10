from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    # Relationship field
    users = relationship("User", secondary="users_skills", back_populates="skills")
    projects = relationship(
        "Project", secondary="project_skills", back_populates="skills"
    )
    experiences = relationship(
        "Experience", secondary="experience_skills", back_populates="skills"
    )
