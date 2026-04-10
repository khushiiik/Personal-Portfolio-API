from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    __table_args__ = (UniqueConstraint("name", "user_id", name="unique_user_skill"),)

    # Relationship field
    user = relationship("User", back_populates="skills")
    projects = relationship(
        "Project", secondary="project_skills", back_populates="skills"
    )
    experiences = relationship(
        "Experience", secondary="experience_skills", back_populates="skills"
    )
