from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from utils import hash_password, get_current_user
from schemas.teacher import TeacherSchema, TeacherResponse
import models

router = APIRouter()

@router.post("/admin/teacher", response_model=TeacherResponse)
def create_teacher(teacher: TeacherSchema, db: Session = Depends(get_db), current_user_data: tuple = Depends(get_current_user)):
    current_user, role = current_user_data
    if role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create teacher accounts")
    
    existing_email = db.query(models.Teacher).filter(models.Teacher.email == teacher.email).first()
    if existing_email:
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
    return db_teacher

@router.get("/teacher/me", response_model=TeacherResponse)
def get_teacher_profile(current_user_data: tuple = Depends(get_current_user)):
    current_user, role = current_user_data
    if role != "teacher":
        raise HTTPException(status_code=403, detail="Not authorized")
    return current_user