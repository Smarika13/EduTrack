from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from utils import get_current_user
from schemas.teacher import TeacherSchema, TeacherResponse
from logger import logger
import services.teacher_service as teacher_service

router = APIRouter()


@router.post("/admin/teacher", response_model=TeacherResponse)
def create_teacher(teacher: TeacherSchema, db: Session = Depends(get_db), current_user_data: tuple = Depends(get_current_user)):
    current_user, role = current_user_data
    if role != "admin":
        logger.warning(f"Unauthorized teacher creation attempt by {current_user.email}")
        raise HTTPException(status_code=403, detail="Only admin can create teacher accounts")
    return teacher_service.create_teacher(teacher, db, current_user)


@router.get("/teacher/me", response_model=TeacherResponse)
def get_teacher_profile(current_user_data: tuple = Depends(get_current_user)):
    current_user, role = current_user_data
    if role != "teacher":
        logger.warning(f"Unauthorized access by {current_user.email}")
        raise HTTPException(status_code=403, detail="Not authorized")
    logger.info(f"Teacher {current_user.email} fetched their profile")
    return current_user
