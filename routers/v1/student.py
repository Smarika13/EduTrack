from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from dependencies import get_db
from utils import get_current_user
from schemas.student import StudentResponse
from schemas.attendance import AttendanceResponse
from schemas.score import ScoreResponse
from schemas.submission import SubmissionResponse
from logger import logger
from schemas.pagination import PaginatedResponse
from caching import get_redis
import services.student_service as student_service

router = APIRouter()


def require_student(current_user_data: tuple = Depends(get_current_user)):
    current_user, role = current_user_data
    if role != "student":
        logger.warning(f"Unauthorized access by {current_user.email}")
        raise HTTPException(status_code=403, detail="Not authorized")
    return current_user


def pagination(page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100)):
    return page, limit


@router.get("/student/me", response_model=StudentResponse)
def get_my_profile(current_user=Depends(require_student)):
    logger.info(f"Student {current_user.email} fetched their profile")
    return current_user


@router.get("/student/me/attendance", response_model=PaginatedResponse[AttendanceResponse])
async def get_my_attendance(current_user=Depends(require_student), db: Session = Depends(get_db), pg=Depends(pagination), cache=Depends(get_redis)):
    return await student_service.get_my_attendance(current_user, db, pg, cache)


@router.get("/student/me/scores", response_model=PaginatedResponse[ScoreResponse])
def get_my_scores(current_user=Depends(require_student), db: Session = Depends(get_db), pg=Depends(pagination)):
    return student_service.get_my_scores(current_user, db, pg)


@router.get("/student/me/submissions", response_model=PaginatedResponse[SubmissionResponse])
def get_my_submissions(current_user=Depends(require_student), db: Session = Depends(get_db), pg=Depends(pagination)):
    return student_service.get_my_submissions(current_user, db, pg)
