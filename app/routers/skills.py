from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.dependencies import get_db, get_current_user

router = APIRouter(prefix="/skills", tags=["Skills"])


@router.get("/", response_model=List[schemas.skill.SkillResponse])
def get_skills(
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_user),
):
    skills = (
        db.query(models.skill.Skill)
        .filter(models.skill.Skill.user_id == current_user.id)
        .all()
    )

    return skills


@router.post("/", response_model=schemas.skill.SkillResponse, status_code=201)
def create_skills(
    skills: schemas.skill.SkillCreate,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_user),
):
    skill_existing = (
        db.query(models.skill.Skill)
        .filter(
            models.skill.Skill.name == skills.name,
            models.skill.Skill.user_id == current_user.id,
        )
        .first()
    )

    if skill_existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Skill already exists!"
        )

    skill = models.skill.Skill(name=skills.name, user_id=current_user.id)

    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


@router.delete("/{skill_id}")
def remove_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_user),
):
    skill = (
        db.query(models.skill.Skill)
        .filter_by(id=skill_id, user_id=current_user.id)
        .first()
    )

    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found!"
        )

    db.delete(skill)
    db.commit()

    return {"message": f"{skill.name} is deleted!"}
