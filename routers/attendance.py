from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from utils import get_current_user
from schemas.attendance import AttendanceSchema, AttendanceResponse
import models

router = APIRouter()

@router.post("/attendance", response_model=AttendanceResponse)
def mark_attendance(attendance: AttendanceSchema, current_user_data: tuple = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user, role = current_user_data
    if role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can mark attendance")
    
    subject = db.query(models.Subject).filter(models.Subject.id == attendance.subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    if subject.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only mark attendance for your own subjects")
    
    student = db.query(models.Student).filter(models.Student.id == attendance.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if student.faculty != subject.faculty:
        raise HTTPException(status_code=400, detail="Student does not belong to this subject's faculty")
    
    existing_attendance = db.query(models.Attendance).filter(
    models.Attendance.student_id == attendance.student_id,
    models.Attendance.subject_id == attendance.subject_id,
    models.Attendance.date == attendance.date).first()
    if existing_attendance:
        raise HTTPException(status_code=400, detail="Attendance already marked for this student on this date")

    
    db_attendance = models.Attendance(
        date=attendance.date,
        status=attendance.status,
        student_id=attendance.student_id,
        subject_id=attendance.subject_id
    )
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance