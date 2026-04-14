from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.dependencies import get_db, get_current_user
from app.services import (
    get_or_create_skill,
    delete_skill_if_unused,
    add_skills_to_model,
    validate_dates,
)

router = APIRouter(prefix="/experience", tags=["Experiences"])


@router.get("/", response_model=List[schemas.experience.ExperienceResponse])
def get_experience(
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_user),
):
    experience = (
        db.query(models.experience.Experience).filter_by(user_id=current_user.id).all()
    )

    return experience


@router.post("/", response_model=schemas.experience.ExperienceResponse, status_code=201)
def create_experience(
    data: schemas.experience.ExperienceCreate,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_user),
):
    experience = models.experience.Experience(
        **data.model_dump(exclude={"skills"}), user_id=current_user.id
    )

    db.add(experience)
    db.flush()

    # handle skills.
    add_skills_to_model(db, data.skills, current_user.id, model=experience)

    db.commit()
    db.refresh(experience)

    return experience


@router.post("/{experience_id}", response_model=schemas.experience.ExperienceResponse)
def add_skill_to_experience(
    experience_id: int,
    data: schemas.experience.ExperienceSkillAdd,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_user),
):
    experience = (
        db.query(models.experience.Experience)
        .filter_by(id=experience_id, user_id=current_user.id)
        .first()
    )

    if not experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Experience not found!"
        )

    existing_skills = {s.name for s in experience.skills}

    for skill_name in data.skills:
        if skill_name not in existing_skills:
            skill = get_or_create_skill(db, skill_name, current_user.id)
            experience.skills.append(skill)

    db.commit()
    db.refresh(experience)
    return experience


@router.patch("/{experience_id}", response_model=schemas.experience.ExperienceResponse)
def update_experience(
    experience_id: int,
    data: schemas.ExperienceUpdate,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_user),
):

    experience = (
        db.query(models.experience.Experience)
        .filter_by(id=experience_id, user_id=current_user.id)
        .first()
    )

    if not experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Experience not found!"
        )

    update_data = data.model_dump(exclude_none=True)

    for field, value in update_data.items():
        setattr(experience, field, value)

    if update_data.get("is_current") is True:
        experience.end_date = None

    validate_dates(experience.start_date, experience.end_date, experience.is_current)
    db.commit()
    db.refresh(experience)
    return experience


@router.delete(
    "/{experience_id}/{skill_id}", response_model=schemas.experience.ExperienceResponse
)
def remove_skills_from_experience(
    experience_id: int,
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_user),
):

    # Get experience.
    experience = (
        db.query(models.experience.Experience)
        .filter_by(id=experience_id, user_id=current_user.id)
        .first()
    )

    if not experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Experience not found!"
        )

    # Get skill.
    skill = (
        db.query(models.skill.Skill)
        .filter_by(id=skill_id, user_id=current_user.id)
        .first()
    )

    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found!"
        )

    # Ensure skill belongs to experience.
    if skill not in experience.skills:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Skill not linked to this experience!",
        )

    # Remove skill from project.
    experience.skills.remove(skill)

    # Check if skill is used in ANY other project
    delete_skill_if_unused(db, skill, user_id=current_user.id)

    db.commit()
    db.refresh(experience)
    return experience


@router.delete("/{experience_id}")
def delete_experience(
    experience_id: int,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_user),
):
    experience = (
        db.query(models.experience.Experience)
        .filter_by(id=experience_id, user_id=current_user.id)
        .first()
    )

    if not experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Experience not found!"
        )

    db.delete(experience)
    db.commit()
    return {"message": "Experience deleted successfully!"}
