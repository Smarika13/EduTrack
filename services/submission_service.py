from fastapi import HTTPException
from fastapi.responses import FileResponse
import models
from datetime import datetime
import uuid
import os


UPLOAD_DIR = "uploads"


def create_submission(assignment_id, file, current_user, db):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    assignment = db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    if datetime.utcnow() > assignment.deadline:
        raise HTTPException(status_code=400, detail="Assignment deadline has passed")

    existing_submission = db.query(models.Submission).filter(
        models.Submission.assignment_id == assignment_id,
        models.Submission.student_id == current_user.id
    ).first()
    if existing_submission:
        raise HTTPException(status_code=400, detail="You have already submitted this assignment")

    unique_filename = f"{uuid.uuid4()}.pdf"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    db_submission = models.Submission(
        status="submitted",
        file_path=file_path,
        submitted_at=datetime.utcnow(),
        assignment_id=assignment_id,
        student_id=current_user.id
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission


def update_submission(assignment_id, file, current_user, db):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    db_submission = db.query(models.Submission).filter(
        models.Submission.assignment_id == assignment_id,
        models.Submission.student_id == current_user.id
    ).first()
    if not db_submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    # Delete old file from disk
    if os.path.exists(db_submission.file_path):
        os.remove(db_submission.file_path)

    unique_filename = f"{uuid.uuid4()}.pdf"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    db_submission.file_path = file_path
    db.commit()
    db.refresh(db_submission)
    return db_submission


def delete_submission(assignment_id, current_user, db):

    db_submission = db.query(models.Submission).filter(
        models.Submission.assignment_id == assignment_id,
        models.Submission.student_id == current_user.id
    ).first()
    if not db_submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    if os.path.exists(db_submission.file_path):
        os.remove(db_submission.file_path)

    db.delete(db_submission)
    db.commit()
    return {"message": "Submission deleted successfully"}


def download_submission(assignment_id, current_user, role, db):

    if role == "student":
        db_submission = db.query(models.Submission).filter(
            models.Submission.assignment_id == assignment_id,
            models.Submission.student_id == current_user.id
        ).first()
    elif role == "teacher":
        db_submission = db.query(models.Submission).filter(
            models.Submission.assignment_id == assignment_id
        ).first()
    else:
        raise HTTPException(status_code=403, detail="Not authorized")

    if not db_submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    if not os.path.exists(db_submission.file_path):
        raise HTTPException(status_code=404, detail="File not found on server")

    return FileResponse(
        path=db_submission.file_path,
        media_type="application/pdf",
        filename=f"submission_{assignment_id}.pdf"
    )
