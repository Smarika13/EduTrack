from fastapi import HTTPException
from logger import logger
import models


def create_assignment(assignment, current_user, db):

    subject = db.query(models.Subject).filter(models.Subject.id == assignment.subject_id).first()
    if not subject:
        logger.warning(f"Subject {assignment.subject_id} not found - requested by {current_user.email}")
        raise HTTPException(status_code=404, detail="Subject not found")

    if subject.teacher_id != current_user.id:
        logger.warning(
            f"Teacher {current_user.email} attempted to create assignment for subject {assignment.subject_id} they don't own")
        raise HTTPException(status_code=403, detail="You can only create assignments for your own subjects")

    db_assignment = models.Assignment(
        title=assignment.title,
        description=assignment.description,
        deadline=assignment.deadline,
        subject_id=assignment.subject_id,
        teacher_id=current_user.id
    )
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    logger.info(f"Successful creation of assignment by {current_user.email}")
    return db_assignment
