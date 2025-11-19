"""
User endpoints: registration and token issuance.
"""
from __future__ import annotations

from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas, services, auth, repositories
from app.config import settings

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register(user_in: schemas.UserCreate, db: Session = Depends(auth.get_db)) -> Any:
    """Register a new user."""
    try:
        user = services.register_user(db, user_in.email, user_in.password)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return user


@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(auth.get_db)
) -> Any:
    """
    Obtain JWT token using username/password (username is email).
    Enforces simple password expiry policy.
    """
    user = services.authenticate_with_policy(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials or password expired")
    access_token = auth.create_access_token(subject=user.email, expires_delta=timedelta(minutes=settings.access_token_expiry))
    return {"access_token": access_token, "token_type": "bearer"}
