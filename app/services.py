"""
Service layer wrapping repository calls with business checks.
"""
from __future__ import annotations

from datetime import datetime, timezone, timedelta

from sqlalchemy.orm import Session

from app import repositories
from app.models import User

PASSWORD_EXPIRY_DAYS = 30

def _ensure_aware_utc(dt: datetime | None) -> datetime:
    """
    Return a timezone-aware UTC datetime.
    - If dt is None -> current UTC now
    - If dt is naive -> assume it was UTC and attach timezone.utc
    - If dt is aware -> convert to UTC
    """
    if dt is None:
        return datetime.now(timezone.utc)
    if dt.tzinfo is None:
        # assume naive timestamps in DB are UTC; attach tzinfo
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


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
    last_change = _ensure_aware_utc(user.last_password_change)
    if last_change + timedelta(days=PASSWORD_EXPIRY_DAYS) < now:
        # password expired
        return None
    return user
