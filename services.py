from fastapi import HTTPException, status
from app import models


# skill_service.
def get_or_create_skill(db, name, user_id):
    """ "Get existing skill or create a new one."""

    # Check if skill already exists for this user.
    skill = db.query(models.skill.Skill).filter_by(name=name, user_id=user_id).first()

    if not skill:
        # Create new skill if not found.
        skill = models.skill.Skill(name=name, user_id=user_id)
        db.add(skill)
        db.flush()

    return skill

# skill_service.
def add_skills_to_model(db, skills, user_id, model):
    """Attach skills to project/experience."""

    for skill_data in skills:
        skill = get_or_create_skill(db, skill_data.name, user_id)
        model.skills.append(skill)


# skill_service.
def delete_skill_if_unused(db, skill, user_id):
    """Delete skill if it's not used in any project or experience."""

    # Check usage in projects.
    project_usage = (
        db.query(models.project.Project)
        .filter(
            models.project.Project.user_id == user_id,
            models.project.Project.skills.any(id=skill.id),
        )
        .first()
    )

    # Check usage in experiences.
    experience_usage = (
        db.query(models.experience.Experience)
        .filter(
            models.experience.Experience.user_id == user_id,
            models.experience.Experience.skills.any(id=skill.id),
        )
        .first()
    )

    # Delete if unused.
    if not project_usage and not experience_usage:
        db.delete(skill)


# project_experience_service.
def validate_dates(start_date, end_date, is_current):
    """Validate date logic for project/experience."""

    if is_current and end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current item cannot have end_date!",
        )

    if start_date and end_date and end_date < start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="end_date must be after start_date!",
        )
