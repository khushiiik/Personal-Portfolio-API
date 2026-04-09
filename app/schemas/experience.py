from pydantic import ConfigDict, Field, BaseModel, model_validator
from typing import List
from .skill import SkillResponse, SkillCreate, SkillUpdate
from datetime import date


# Experience Schemas.
class ExperienceCreate(BaseModel):
    role: str
    company: str
    description: str | None = None
    start_date: date
    end_date: date | None = None
    is_current: bool
    skills: List[SkillCreate] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_dates(self):
        """Ensure valid experience date logic."""

        if self.is_current and self.end_date:
            raise ValueError("Current experience cannot have end_date!")

        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError("end_date must be after start_date!")

        return self


class ExperienceUpdate(BaseModel):
    role: str | None = None
    company: str | None = None
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    is_current: bool
    skills: List[SkillUpdate] | None = None


class ExperienceResponse(BaseModel):
    id: int
    role: str
    company: str
    description: str | None = None
    start_date: date
    end_date: date | None = None
    is_current: bool
    skills: List[SkillResponse] = Field(default_factory=list)

    # For pydantic to read SQLAlchemy objects.
    model_config = ConfigDict(from_attributes=True)
