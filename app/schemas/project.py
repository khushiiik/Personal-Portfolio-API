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
    def validate_dates(cls, values):
        """Ensure valid project date logic."""

        if values.is_current and values.end_date:
            raise ValueError("Current project cannot have end_date!")

        if (
            values.start_date
            and values.end_date
            and values.end_date < values.start_date
        ):
            raise ValueError("end_date must be after start_date!")

        return values


class ProjectUpdate(BaseModel):
    title: str | None = None
    project_link: str | None = None
    description: str | None = None
    is_current: bool | None = None
    start_date: date | None = None
    end_date: date | None = None
    skills: List[SkillUpdate] | None = None

    @model_validator(mode="after")
    def validate_dates(cls, values):
        if values.is_current is True and values.end_date is not None:
            raise ValueError("Current project cannot have end_date!")

        if (
            values.start_date is not None
            and values.end_date is not None
            and values.end_date < values.start_date
        ):
            raise ValueError("end_date must be after start_date!")

        return values


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
