import models
from fastapi import HTTPException


def create_subject(subject, db):

    teacher = db.query(models.Teacher).filter(models.Teacher.id == subject.teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    if teacher.faculty != subject.faculty:
        raise HTTPException(status_code=400, detail="Teacher does not belong to this faculty")

    db_subject = models.Subject(
        name=subject.name,
        credit_hr=subject.credit_hr,
        faculty=subject.faculty,
        semester=subject.semester,
        teacher_id=subject.teacher_id
    )
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject
