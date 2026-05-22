from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from dependencies import get_db
from utils import get_current_user
from schemas.submission import SubmissionResponse
import services.submission_service as submission_service

router = APIRouter()


@router.post("/submission", response_model=SubmissionResponse)
def create_submission(
    assignment_id: int = Form(...),
    file: UploadFile = File(...),
    current_user_data: tuple = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user, role = current_user_data
    if role != "student":
        raise HTTPException(status_code=403, detail="Not authorized")

    return submission_service.create_submission(assignment_id, file, current_user, db)


@router.put("/submission/assignment/{assignment_id}", response_model=SubmissionResponse)
def update_submission(
    assignment_id: int,
    file: UploadFile = File(...),
    current_user_data: tuple = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user, role = current_user_data
    if role != "student":
        raise HTTPException(status_code=403, detail="Not authorized")
    return submission_service.update_submission(assignment_id, file, current_user, db)


@router.delete("/submission/assignment/{assignment_id}")
def delete_submission(
    assignment_id: int,
    current_user_data: tuple = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user, role = current_user_data
    if role != "student":
        raise HTTPException(status_code=403, detail="Not authorized")
    return submission_service.delete_submission(assignment_id, current_user, db)


@router.get("/submission/assignment/{assignment_id}/download")
def download_submission(
    assignment_id: int,
    current_user_data: tuple = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user, role = current_user_data

    return submission_service.download_submission(assignment_id, current_user, role, db)
