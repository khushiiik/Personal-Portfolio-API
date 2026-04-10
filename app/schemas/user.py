from pydantic import BaseModel, Field, EmailStr, ConfigDict


# Auth Schemas.
class UserCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    email: str = Field(min_length=5)
    password: str = Field(min_length=6)


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    # For pydantic to read SQLAlchemy objects.
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    name: str | None = None

class Token(BaseModel):
    access_token: str
    token_type: str
