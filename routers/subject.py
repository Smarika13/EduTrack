from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from utils import get_current_user
from schemas.subject import SubjectSchema, SubjectResponse
import models

router = APIRouter()

@router.post("/subject", response_model=SubjectResponse)
def create_subject(subject: SubjectSchema, current_user_data: tuple = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user, role = current_user_data
    if role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create subjects")
    
    teacher = db.query(models.Teacher).filter(models.Teacher.id == subject.teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    if teacher.faculty != subject.faculty:
        raise HTTPException(status_code=400, detail="Teacher does not belong to this faculty")
    
    db_subject = models.Subject(
        name=subject.name,
        credit_hr=subject.credit_hr,
        faculty=subject.faculty,
        semester=subject.semester,
        teacher_id=subject.teacher_id
    )
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject