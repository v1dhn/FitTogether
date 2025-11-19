"""
Workout endpoints: create (protected) and list (public).
"""
from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import schemas, auth, repositories
from app.models import User

router = APIRouter(prefix="/workouts", tags=["workouts"])


@router.post("/", response_model=schemas.WorkoutOut)
def create_workout(
    payload: schemas.WorkoutCreate,
    db: Session = Depends(auth.get_db),
    current_user: User = Depends(auth.get_current_user),
) -> schemas.WorkoutOut:
    """Create a workout for the authenticated user."""
    workout = repositories.create_workout(db, current_user, payload.title, payload.description)
    return workout


@router.get("/", response_model=List[schemas.WorkoutOut])
def list_workouts(
    limit: int = Query(20, gt=0, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(auth.get_db),
) -> list[schemas.WorkoutOut]:
    """List workouts (paginated)."""
    return repositories.list_workouts(db, limit=limit, offset=offset)
