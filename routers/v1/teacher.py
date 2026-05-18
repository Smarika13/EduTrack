from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from utils import hash_password, get_current_user
from schemas.teacher import TeacherSchema, TeacherResponse
import models
from logger import logger

router = APIRouter()

@router.post("/admin/teacher", response_model=TeacherResponse)
def create_teacher(teacher: TeacherSchema, db: Session = Depends(get_db), current_user_data: tuple = Depends(get_current_user)):
    current_user, role = current_user_data
    if role != "admin":
        logger.warning(f"Unauthorized teacher creation attempt by {current_user.email}")
        raise HTTPException(status_code=403, detail="Only admin can create teacher accounts")
    
    existing_email = db.query(models.Teacher).filter(models.Teacher.email == teacher.email).first()
    if existing_email:
       logger.warning(f"Teacher creation failed - email already registered: {teacher.email}")
       raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(teacher.password)
    db_teacher = models.Teacher(
        name=teacher.name,
        email=teacher.email,
        phone=teacher.phone,
        department=teacher.department,
        faculty=teacher.faculty,
        qualification=teacher.qualification,
        hashed_password=hashed
    )
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    logger.info(f"Admin {current_user.email} created teacher {teacher.email}")
    return db_teacher

@router.get("/teacher/me", response_model=TeacherResponse)
def get_teacher_profile(current_user_data: tuple = Depends(get_current_user)):
    current_user, role = current_user_data
    if role != "teacher":
        logger.warning(f"Unauthorized access by {current_user.email}")
        raise HTTPException(status_code=403, detail="Not authorized")
    logger.info(f"Teacher {current_user.email} fetched their profile")
    return current_user