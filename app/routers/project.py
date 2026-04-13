from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.dependencies import get_db, get_current_user
from services import (
    get_or_create_skill,
    delete_skill_if_unused,
    add_skills_to_model,
    validate_dates,
)

router = APIRouter(prefix="/project", tags=["Projects"])


@router.get("/", response_model=List[schemas.project.ProjectResponse])
def get_projects(
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_user),
):
    projects = db.query(models.project.Project).filter_by(user_id=current_user.id).all()

    return projects


@router.post("/", response_model=schemas.project.ProjectResponse, status_code=201)
def create_project(
    data: schemas.project.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_user),
):

    project = models.project.Project(
        **data.model_dump(exclude={"skills"}), user_id=current_user.id
    )

    db.add(project)
    db.flush()

    # handle skills.
    add_skills_to_model(db, data.skills, current_user.id, model=project)

    db.commit()
    db.refresh(project)
    return project


@router.post("/{project_id}", response_model=schemas.project.ProjectResponse)
def add_skill_to_project(
    project_id: int,
    data: schemas.project.ProjectSkillAdd,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_user),
):
    project = (
        db.query(models.project.Project)
        .filter_by(id=project_id, user_id=current_user.id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found!"
        )

    existing_skills = {s.name for s in project.skills}

    for skill_name in data.skills:
        if skill_name not in existing_skills:
            skill = get_or_create_skill(db, skill_name, current_user.id)
            project.skills.append(skill)

    db.commit()
    db.refresh(project)
    return project


@router.patch("/{project_id}", response_model=schemas.project.ProjectResponse)
def update_project(
    project_id: int,
    data: schemas.project.ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_user),
):
    project = (
        db.query(models.project.Project)
        .filter_by(id=project_id, user_id=current_user.id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found!"
        )

    update_data = data.model_dump(exclude_none=True)

    for field, value in update_data.items():
        setattr(project, field, value)

    if update_data.get("is_current") is True:
        project.end_date = None

    if project.is_current and project.end_date:
        raise HTTPException(
            status_code=400, detail="Current project cannot have end_date!"
        )

    validate_dates(project.start_date, project.end_date, project.is_current)

    db.commit()
    db.refresh(project)
    return project


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_user),
):
    project = (
        db.query(models.project.Project)
        .filter_by(id=project_id, user_id=current_user.id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found!"
        )

    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully!"}


@router.delete(
    "/{project_id}/{skill_id}", response_model=schemas.project.ProjectResponse
)
def remove_skills_from_project(
    project_id: int,
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_user),
):

    # Get project.
    project = (
        db.query(models.project.Project)
        .filter_by(id=project_id, user_id=current_user.id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found!"
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

    # Ensure skill belongs to project.
    if skill not in project.skills:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Skill not linked to this project!",
        )

    # Remove skill from project.
    project.skills.remove(skill)

    # Check if skill is used in ANY other project
    delete_skill_if_unused(db, skill, user_id=current_user.id)

    db.commit()
    db.refresh(project)
    return project
