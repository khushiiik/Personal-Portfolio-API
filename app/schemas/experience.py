from pydantic import ConfigDict, Field, BaseModel, model_validator
from typing import List
from .skill import SkillResponse, SkillCreate
from datetime import date
from services import validate_dates


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
        validate_dates(self.start_date, self.end_date, self.is_current)
        return self


class ExperienceUpdate(BaseModel):
    role: str | None = None
    company: str | None = None
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    is_current: bool | None = None

    @model_validator(mode="after")
    def validate_dates(self):
        if any(
            [
                self.start_date is not None,
                self.end_date is not None,
                self.is_current is not None,
            ]
        ):
            validate_dates(self.start_date, self.end_date, self.is_current)
        return self


class ExperienceSkillAdd(BaseModel):
    skills: list[str]


class ExperienceSkillRemove(BaseModel):
    skills: list[str]


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
