from fastapi import HTTPException
import models
from logger import logger


async def mark_attendance(attendance, current_user, db, cache):
    subject = db.query(models.Subject).filter(models.Subject.id == attendance.subject_id).first()
    if not subject:
        logger.warning(f"Subject {attendance.subject_id} not found - requested by {current_user.email}")
        raise HTTPException(status_code=404, detail="Subject not found")

    if subject.teacher_id != current_user.id:
        logger.warning(
            f"Teacher {current_user.email} attempted to mark attendance for subject {attendance.subject_id} they don't own")
        raise HTTPException(status_code=403, detail="You can only mark attendance for your own subjects")

    student = db.query(models.Student).filter(models.Student.id == attendance.student_id).first()
    if not student:
        logger.warning(f"Student {attendance.student_id} not found - requested by {current_user.email}")
        raise HTTPException(status_code=404, detail="Student not found")

    if student.faculty != subject.faculty:
        logger.warning(
            f"Student {attendance.student_id} faculty {student.faculty} doesn't match subject {attendance.subject_id} faculty {subject.faculty}")
        raise HTTPException(status_code=400, detail="Student does not belong to this subject's faculty")

    existing_attendance = db.query(models.Attendance).filter(
        models.Attendance.student_id == attendance.student_id,
        models.Attendance.subject_id == attendance.subject_id,
        models.Attendance.date == attendance.date).first()
    if existing_attendance:
        logger.warning(
            f"Duplicate attendance - student {attendance.student_id} already marked for subject {attendance.subject_id} on {attendance.date}")
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
    cache_key = (f"attendance:{attendance.student_id}")
    await cache.delete(cache_key)
    logger.info(f"{current_user.email} has successfully deleted {cache_key}")
    logger.info(f"{current_user.email} has successfully marked {attendance.student_id} from {subject.faculty}")
    return db_attendance
