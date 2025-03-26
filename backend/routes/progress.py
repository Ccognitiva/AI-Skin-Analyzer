from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Progress
from schemas import ProgressCreate, ProgressResponse
from database import get_db
from dependencies import get_current_user

router = APIRouter(prefix="/progress", tags=["Progress"])

@router.post("/", response_model=ProgressResponse)
def add_progress(progress: ProgressCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    new_progress = Progress(user_id=user.id, condition=progress.condition, improvement=progress.improvement)
    db.add(new_progress)
    db.commit()
    db.refresh(new_progress)
    return new_progress

@router.get("/", response_model=list[ProgressResponse])
def get_progress(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Progress).filter(Progress.user_id == user.id).all()
