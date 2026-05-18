from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from utils import get_current_user
from schemas.test import TestSchema, TestResponse
import models

router = APIRouter()

@router.post("/test", response_model=TestResponse)
def create_test(test: TestSchema, current_user_data: tuple = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user, role = current_user_data
    if role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can create tests")
    
    subject = db.query(models.Subject).filter(models.Subject.id == test.subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    if subject.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only create tests for your own subjects")
    
    db_test = models.Test(
        name=test.name,
        full_mark=test.full_mark,
        pass_mark=test.pass_mark,
        date=test.date,
        subject_id=test.subject_id
    )
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test