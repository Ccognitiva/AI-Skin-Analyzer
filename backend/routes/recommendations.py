from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Recommendation, User
from schemas import RecommendationResponse
from database import get_db
from dependencies import get_current_user

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.get("/", response_model=list[RecommendationResponse])
def get_recommendations(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    recommendations = db.query(Recommendation).filter(Recommendation.user_id == user.id).all()
    if not recommendations:
        raise HTTPException(status_code=404, detail="No recommendations found")
    return recommendations
