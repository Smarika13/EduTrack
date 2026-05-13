from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from dependencies import get_db
from utils import get_current_user
from schemas.student import StudentResponse
from schemas.attendance import AttendanceResponse
from schemas.score import ScoreResponse
from schemas.submission import SubmissionResponse
from typing import List
import models

router = APIRouter()

@router.get("/student/me", response_model=StudentResponse)
def get_my_profile(current_user_data: tuple = Depends(get_current_user)):
    current_user, role = current_user_data
    if role != "student":
        raise HTTPException(status_code=403, detail="Not authorized")
    return current_user

@router.get("/student/me/attendance", response_model=List[AttendanceResponse])
def get_my_attendance(
    current_user_data: tuple = Depends(get_current_user),
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    current_user, role = current_user_data
    if role != "student":
        raise HTTPException(status_code=403, detail="Not authorized")
    offset = (page - 1) * limit
    return db.query(models.Attendance).filter(
        models.Attendance.student_id == current_user.id
    ).offset(offset).limit(limit).all()

@router.get("/student/me/scores", response_model=List[ScoreResponse])
def get_my_scores(
    current_user_data: tuple = Depends(get_current_user),
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    current_user, role = current_user_data
    if role != "student":
        raise HTTPException(status_code=403, detail="Not authorized")
    offset = (page - 1) * limit
    return db.query(models.Score).filter(
        models.Score.student_id == current_user.id
    ).offset(offset).limit(limit).all()

@router.get("/student/me/submissions", response_model=List[SubmissionResponse])
def get_my_submissions(
    current_user_data: tuple = Depends(get_current_user),
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    current_user, role = current_user_data
    if role != "student":
        raise HTTPException(status_code=403, detail="Not authorized")
    offset = (page - 1) * limit
    return db.query(models.Submission).filter(
        models.Submission.student_id == current_user.id
    ).offset(offset).limit(limit).all()