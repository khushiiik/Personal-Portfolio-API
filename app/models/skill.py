from sqlalchemy import (Column, Integer, String, ForeignKey, Boolean)
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone

class Skill(Base):
    __tablename__ = "skills"

    # Primary key field.
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)
    