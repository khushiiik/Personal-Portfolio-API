from pydantic import BaseModel, ConfigDict, field_validator


# Skill Schemas.
class SkillCreate(BaseModel):
    name: str

    @field_validator("name")
    def normalize_name(cls, value):
        """Clean and normalize skill name."""

        if value:
            return value.strip().lower()

        return value


class SkillResponse(BaseModel):
    id: int
    name: str

    # For pydantic to read SQLAlchemy objects.
    model_config = ConfigDict(from_attributes=True)
