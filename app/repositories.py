"""
Repository functions for simple CRUD operations.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Return a user by email or None if not found."""
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, email: str, password: str) -> models.User:
    """Create and persist a new user with a hashed password."""
    hashed = pwd_context.hash(password)
    now = datetime.now(timezone.utc)
    user = models.User(
        email=email, hashed_password=hashed, created_at=now, last_password_change=now
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against the hashed value."""
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, email: str, password: str) -> Optional[models.User]:
    """Authenticate a user by email and password; return user if valid."""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_workout(
    db: Session, user: models.User, title: str, description: str | None
) -> models.Workout:
    """Create a workout for the given user."""
    workout = models.Workout(
        user_id=user.id, title=title, description=description, created_at=datetime.now(timezone.utc)
    )
    db.add(workout)
    db.commit()
    db.refresh(workout)
    return workout


def list_workouts(db: Session, limit: int = 20, offset: int = 0) -> List[models.Workout]:
    """Return paginated workouts ordered newest first."""
    return (
        db.query(models.Workout)
        .order_by(models.Workout.created_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )
