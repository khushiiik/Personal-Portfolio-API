from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.dependencies import get_current_user, get_db

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/{user_id}", response_model=schemas.user.UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_user),
):
    user = db.query(models.user.User).filter(models.user.User.id == user_id).first()

    if not user:
        raise HTTPException(404, "User not found!")

    if user.id != current_user.id:
        if current_user.role != "admin":
            raise HTTPException(404, "User not found!")

    return user

@router.patch("/{user_id}", response_model=schemas.user.UserResponse)
def update_user_name(user_id: int, data: schemas.user.UserUpdate, db: Session = Depends(get_db), current_user: models.user.User = Depends(get_current_user)):
    user = db.query(models.user.User).filter(models.user.User.id == user_id).first()

    if not user:
        raise HTTPException(404, "User not found!")
    
    if user.id != current_user.id:
        raise HTTPException(404,"User not found!")
    
    update_name = data.model_dump(exclude_none=True)
    for field, value in update_name.items():
        setattr(user, field, value)

        db.commit()
        db.refresh(user)
        return user