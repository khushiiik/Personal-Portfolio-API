from sqlalchemy import Column, Integer, String, Date, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from . import experience_skills


class Experience(Base):
    __tablename__ = "experiences"

    # Primary key field.
    id = Column(Integer, primary_key=True, index=True)

    role = Column(String, nullable=False)
    company = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    is_archived = Column(Boolean, default=False)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Experience Count.
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)

    # Currently working.
    is_current = Column(Boolean, default=False)

    # Relationship Field.
    user = relationship("User", back_populates="experiences")
    skills = relationship(
        "Skill", secondary=experience_skills, back_populates="experiences"
    )
