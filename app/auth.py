"""
Authentication utilities: JWT creation/validation and dependency.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app import repositories
from app.config import settings
from app.db import SessionLocal
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


def get_db() -> Generator[Session, None, None]:
    """Yield a DB session and ensure closure."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token for the given subject (user email).
    """
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.access_token_expiry))
    to_encode = {"sub": subject, "exp": int(expire.timestamp())}
    encoded = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return encoded


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    FastAPI dependency that returns the current user or raises 401.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = repositories.get_user_by_email(db, email)
    if user is None:
        raise credentials_exception
    return user
