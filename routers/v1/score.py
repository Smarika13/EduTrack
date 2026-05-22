from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from utils import get_current_user
from schemas.score import ScoreSchema, ScoreResponse
import services.score_service as score_service

router = APIRouter()


@router.post("/score", response_model=ScoreResponse)
def enter_score(score: ScoreSchema, current_user_data: tuple = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user, role = current_user_data
    if role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can enter scores")
    return score_service.enter_score(score, current_user, db)
