from fastapi import HTTPException
import models


def enter_score(score, current_user, db):

    test = db.query(models.Test).filter(models.Test.id == score.test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    subject = db.query(models.Subject).filter(models.Subject.id == test.subject_id).first()
    if subject.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only enter scores for your own subjects")

    student = db.query(models.Student).filter(models.Student.id == score.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    existing_score = db.query(models.Score).filter(
        models.Score.student_id == score.student_id,
        models.Score.test_id == score.test_id
    ).first()
    if existing_score:
        raise HTTPException(status_code=400, detail="Score already recorded for this student in this test")

    if score.marks > test.full_mark:
        raise HTTPException(status_code=400, detail=f"Marks cannot exceed full mark of {test.full_mark}")

    status = "pass" if score.marks >= test.pass_mark else "fail"

    db_score = models.Score(
        marks=score.marks,
        status=status,
        test_id=score.test_id,
        student_id=score.student_id
    )
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score
