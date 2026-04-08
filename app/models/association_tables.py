from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database import Base

project_skills = Table(
    "project_skills",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("projects.id", ondelete="CASCADE")),
    Column("skill_id", Integer, ForeignKey("skills.id", ondelete="CASCADE")),
)

