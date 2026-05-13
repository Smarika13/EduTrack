from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from utils import get_current_user
from schemas.assignment import AssignmentSchema, AssignmentResponse
import models

router = APIRouter()

@router.post("/assignment", response_model=AssignmentResponse)
def create_assignment(assignment: AssignmentSchema, current_user_data: tuple = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user, role = current_user_data
    if role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can create assignments")
    
    subject = db.query(models.Subject).filter(models.Subject.id == assignment.subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    if subject.teacher_id != current_user.id:
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
    return db_assignment