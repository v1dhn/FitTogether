from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Request schema for registering a user."""

    email: EmailStr
    password: str


class UserOut(BaseModel):
    """Response schema for returning user information."""

    id: int
    email: EmailStr
    is_admin: bool
    is_private: bool
    created_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    """JWT token response schema."""

    access_token: str
    token_type: str = "bearer"


class WorkoutCreate(BaseModel):
    """Payload for creating a workout."""

    title: str
    description: Optional[str] = None


class WorkoutOut(BaseModel):
    """Response schema for a workout."""

    id: int
    user_id: int
    title: str
    description: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
