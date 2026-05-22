from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from utils import get_current_user
from schemas.subject import SubjectSchema, SubjectResponse
import services.subject_service as subject_service

router = APIRouter()


@router.post("/subject", response_model=SubjectResponse)
def create_subject(subject: SubjectSchema, current_user_data: tuple = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user, role = current_user_data
    if role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create subjects")

    return subject_service.create_subject(subject, db)
