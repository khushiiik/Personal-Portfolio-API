from pydantic import BaseModel, ConfigDict
from typing import List


class SkillName(BaseModel):
    name: str


class ProjectProfile(BaseModel):
    title: str
    description: str | None = None
    skills: List[SkillName]

    model_config = ConfigDict(from_attributes=True)


class ExperienceProfile(BaseModel):
    role: str
    company: str
    skills: List[SkillName]

    model_config = ConfigDict(from_attributes=True)


class UserProfile(BaseModel):
    name: str
    projects: List[ProjectProfile]
    experiences: List[ExperienceProfile]
    skills: List[SkillName]

    model_config = ConfigDict(from_attributes=True)
