from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.db import Base


EMAIL_MAX_LENGTH: int = 255
PASSWORD_HASH_MAX_LENGTH: int = 255
TITLE_MAX_LENGTH: int = 255


class User(Base):
    """
    User model for registered users.

    Fields:
    - id: Primary key.
    - email: Unique user email (login).
    - hashed_password: Password hash (bcrypt).
    - is_admin: Admin flag for role checks.
    - is_private: Whether profile/workouts are private.
    - created_at: Account creation timestamp.
    - last_password_change: Timestamp of the last password update (for expiry).
    """

    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    email: str = Column(String(EMAIL_MAX_LENGTH), unique=True, index=True, nullable=False)
    hashed_password: str = Column(String(PASSWORD_HASH_MAX_LENGTH), nullable=False)
    is_admin: bool = Column(Boolean, default=False, nullable=False)
    is_private: bool = Column(Boolean, default=False, nullable=False)
    created_at: datetime = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    last_password_change: datetime = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    # relationships
    workouts = relationship("Workout", back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email} admin={self.is_admin}>"


class Workout(Base):
    """
    Workout model representing a user's workout entry.

    Fields:
    - id: Primary key.
    - user_id: ForeignKey to users.id.
    - title: Short title for the workout.
    - description: Optional longer text.
    - created_at: When the workout was logged.
    """

    __tablename__ = "workouts"

    id: int = Column(Integer, primary_key=True, index=True)
    user_id: int = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title: str = Column(String(TITLE_MAX_LENGTH), nullable=False)
    description: str | None = Column(Text, nullable=True)
    created_at: datetime = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # relationships
    owner = relationship("User", back_populates="workouts")

    def __repr__(self) -> str:
        return f"<Workout id={self.id} title={self.title!r} user_id={self.user_id}>"
