from fastapi import HTTPException
import models


def create_test(test, current_user, db):

    subject = db.query(models.Subject).filter(models.Subject.id == test.subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    if subject.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only create tests for your own subjects")

    db_test = models.Test(
        name=test.name,
        full_mark=test.full_mark,
        pass_mark=test.pass_mark,
        date=test.date,
        subject_id=test.subject_id
    )
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test
