from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from utils import get_current_user
from schemas.assignment import AssignmentSchema, AssignmentResponse
from logger import logger
import services.assignment_service as assignment_service

router = APIRouter()


@router.post("/assignment", response_model=AssignmentResponse)
def create_assignment(assignment: AssignmentSchema, current_user_data: tuple = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user, role = current_user_data
    if role != "teacher":
        logger.warning(f"Unauthorized access by {current_user.email}")
        raise HTTPException(status_code=403, detail="Only teachers can create assignments")
    return assignment_service.create_assignment(assignment, current_user, db)
