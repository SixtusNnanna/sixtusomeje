from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from app.core.enum import Role


class UserBase(BaseModel):
    email: EmailStr
    is_active: Optional[bool] = True  # noqa: UP045


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    role: Role = Role.staff

    class Config:
        model_config = ConfigDict(from_attributes=True)
