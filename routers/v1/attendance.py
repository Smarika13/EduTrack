from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from utils import get_current_user
from schemas.attendance import AttendanceSchema, AttendanceResponse
from logger import logger
from caching import get_redis
import services.attendance_service as attendance_service

router = APIRouter()


@router.post("/attendance", response_model=AttendanceResponse)
async def mark_attendance(attendance: AttendanceSchema, current_user_data: tuple = Depends(get_current_user),
                          db: Session = Depends(get_db), cache=Depends(get_redis)):

    current_user, role = current_user_data
    if role != "teacher":
        logger.warning(f"{current_user.email} has unauthorized access for marking")
        raise HTTPException(status_code=403, detail="Only teachers can mark attendance")

    return await attendance_service.mark_attendance(attendance, current_user, db, cache)
