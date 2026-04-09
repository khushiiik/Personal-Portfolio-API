from pydantic import ConfigDict, BaseModel, model_validator, Field
from typing import List
from datetime import date
from .skill import SkillResponse, SkillCreate, SkillUpdate


# Project Schemas.
class ProjectCreate(BaseModel):
    title: str
    project_link: str | None = None
    description: str | None = None
    is_current: bool = False
    start_date: date | None = None
    end_date: date | None = None
    skills: List[SkillCreate] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_dates(self):
        """Ensure valid project date logic."""

        if self.is_current and self.end_date:
            raise ValueError("Current project cannot have end_date!")

        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError("end_date must be after start_date!")

        return self


class ProjectUpdate(BaseModel):
    title: str | None = None
    project_link: str | None = None
    description: str | None = None
    is_current: bool | None = None
    start_date: date | None = None
    end_date: date | None = None
    skills: List[SkillUpdate] | None = None


class ProjectResponse(BaseModel):
    id: int
    title: str
    project_link: str | None = None
    description: str | None = None
    is_current: bool
    start_date: date | None = None
    end_date: date | None = None
    skills: List[SkillResponse] = Field(default_factory=list)

    # For pydantic to read SQLAlchemy objects.
    model_config = ConfigDict(from_attributes=True)
