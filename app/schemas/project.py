from pydantic import ConfigDict, BaseModel, model_validator, Field
from typing import List
from datetime import date
from .skill import SkillResponse, SkillCreate
from services import validate_dates


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
        validate_dates(self.start_date, self.end_date, self.is_current)
        return self


class ProjectUpdate(BaseModel):
    title: str | None = None
    project_link: str | None = None
    description: str | None = None
    is_current: bool | None = None
    start_date: date | None = None
    end_date: date | None = None

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


class ProjectSkillAdd(BaseModel):
    skills: list[str]


class ProjectSkillRemove(BaseModel):
    skills: list[str]


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
