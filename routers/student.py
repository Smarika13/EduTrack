from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from utils import get_current_user
from schemas.student import StudentResponse
from schemas.attendance import AttendanceResponse
from schemas.score import ScoreResponse
from schemas.submission import SubmissionSchema, SubmissionResponse
from datetime import datetime
from typing import List
import models

router = APIRouter()

@router.get("/student/me", response_model=StudentResponse)
def get_my_profile(current_user_data: tuple = Depends(get_current_user)):
    current_user, role = current_user_data
    if role != "student":
        raise HTTPException(status_code=403, detail="Not authorized")
    return current_user

@router.get("/student/me/attendance")
def get_my_attendance(current_user_data: tuple = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user, role = current_user_data
    if role != "student":
        raise HTTPException(status_code=403, detail="Not authorized")
    attendance = db.query(models.Attendance).filter(models.Attendance.student_id == current_user.id).all()
    return attendance

@router.get("/student/me/scores")
def get_my_scores(current_user_data: tuple = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user, role = current_user_data
    if role != "student":
        raise HTTPException(status_code=403, detail="Not authorized")
    scores = db.query(models.Score).filter(models.Score.student_id == current_user.id).all()
    return scores

@router.get("/student/me/submissions")
def get_my_submissions(current_user_data: tuple = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user, role = current_user_data
    if role != "student":
        raise HTTPException(status_code=403, detail="Not authorized")
    submissions = db.query(models.Submission).filter(models.Submission.student_id == current_user.id).all()
    return submissions

@router.post("/submission", response_model=SubmissionResponse)
def create_submission(submission: SubmissionSchema, current_user_data: tuple = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user, role = current_user_data
    if role != "student":
        raise HTTPException(status_code=403, detail="Not authorized")
    db_submission = models.Submission(
        status=submission.status,
        file_path=submission.file_path,
        submitted_at=datetime.utcnow(),
        assignment_id=submission.assignment_id,
        student_id=current_user.id
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission

@router.put("/submission/{submission_id}", response_model=SubmissionResponse)
def update_submission(submission_id: int, submission: SubmissionSchema, current_user_data: tuple = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user, role = current_user_data
    if role != "student":
        raise HTTPException(status_code=403, detail="Not authorized")
    db_submission = db.query(models.Submission).filter(models.Submission.id == submission_id).first()
    if not db_submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    if db_submission.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only update your own submissions")
    db_submission.status = submission.status
    db_submission.file_path = submission.file_path
    db_submission.assignment_id = submission.assignment_id
    db.commit()
    db.refresh(db_submission)
    return db_submission

@router.delete("/submission/{submission_id}")
def delete_submission(submission_id: int, current_user_data: tuple = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user, role = current_user_data
    if role != "student":
        raise HTTPException(status_code=403, detail="Not authorized")
    db_submission = db.query(models.Submission).filter(models.Submission.id == submission_id).first()
    if not db_submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    if db_submission.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own submissions")
    db.delete(db_submission)
    db.commit()
    return {"message": "Submission deleted successfully"}