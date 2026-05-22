from fastapi import HTTPException
import models
from utils import hash_password
from logger import logger


def create_teacher(teacher, db, current_user):

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
