from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app import models, schemas
from app.dependencies import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[schemas.user.UserPublic])
def get_users(db: Session = Depends(get_db)):

    profile = db.query(models.user.User).filter_by(is_active=True).all()

    return profile


@router.get("/{user_id}", response_model=schemas.profile.UserProfile)
def get_user_details(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(models.user.User).filter_by(id=user_id).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found!"
        )

    return profile
