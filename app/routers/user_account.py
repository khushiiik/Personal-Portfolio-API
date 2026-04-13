from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.dependencies import get_current_user, get_db

router = APIRouter(prefix="/account", tags=["Accounts"])


@router.get("/", response_model=schemas.user.UserResponse)
def get_user_account(
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_user),
):
    user_account = db.query(models.user.User).filter_by(id=current_user.id).first()

    if not user_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User account not found!"
        )

    return user_account


@router.get("/profile", response_model=schemas.profile.UserProfile)
def get_user_account_profile(
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_user),
):
    profile = db.query(models.user.User).filter_by(id=current_user.id).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found!"
        )

    return profile


@router.patch("/", response_model=schemas.user.UserResponse)
def update_user_account(
    data: schemas.user.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_user),
):
    user = (
        db.query(models.user.User)
        .filter_by(
            id=current_user.id,
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found!"
        )

    update_data = data.model_dump(exclude_none=True)

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user
