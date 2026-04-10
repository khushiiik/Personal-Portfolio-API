from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.dependencies import get_db, get_current_user, require_admin

router = APIRouter(prefix="/project", tags=["Projects"])


@router.get("/", response_model=List[schemas.project.ProjectResponse])
def get_projects(
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_user),
):
    projects = (
        db.query(models.project.Project)
        .filter(models.project.Project.user_id == current_user.id)
        .all()
    )

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
    for skill_data in data.skills:
        skill = (
            db.query(models.skill.Skill)
            .filter_by(name=skill_data.name, user_id=current_user.id)
            .first()
        )

        if not skill:
            skill = models.skill.Skill(name=skill_data.name, user_id=current_user.id)

            db.add(skill)
            db.flush()

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

    update_project = data.model_dump(exclude_none=True, exclude={"skills"})

    for field, value in update_project.items():
        setattr(project, field, value)
        
    if data.skills is not None:
        # Existing skills on project.
        existing_skills = {s.name: s for s in project.skills}

        # Incoming skills.
        incoming_names = {s.name for s in data.skills}

        # Remove skills not in request.
        for skill in list(project.skills):
            if skill.name not in incoming_names:
                project.skills.remove(skill)

        # Add new skills.
        for skill_data in data.skills:
            if skill_data.name not in existing_skills:
                skill = db.query(models.skill.Skill).filter_by(
                    name=skill_data.name,
                    user_id=current_user.id
                ).first()

                if not skill:
                    skill = models.skill.Skill(
                        name=skill_data.name,
                        user_id=current_user.id
                    )
                    db.add(skill)
                    db.flush()

                project.skills.append(skill)

    db.commit()
    db.refresh(project)
    return project
