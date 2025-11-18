"""
Service layer wrapping repository calls with business checks.
"""
from __future__ import annotations

from datetime import datetime, timezone, timedelta

from sqlalchemy.orm import Session

from app import repositories
from app.models import User

PASSWORD_EXPIRY_DAYS = 30


def register_user(db: Session, email: str, password: str) -> User:
    """
    Register a new user. Raises ValueError if email already exists.
    """
    existing = repositories.get_user_by_email(db, email)
    if existing:
        raise ValueError("Email already registered")
    return repositories.create_user(db, email, password)


def authenticate_with_policy(db: Session, email: str, password: str) -> User | None:
    """
    Authenticate and enforce password expiry policy:
    if last_password_change older than PASSWORD_EXPIRY_DAYS, return None.
    """
    user = repositories.authenticate_user(db, email, password)
    if not user:
        return None
    now = datetime.now(timezone.utc)
    if user.last_password_change + timedelta(days=PASSWORD_EXPIRY_DAYS) < now:
        # password expired
        return None
    return user
