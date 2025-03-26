from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User, Consultation
from schemas import UserResponse, ConsultationResponse
from database import get_db
from dependencies import get_admin_user

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    return db.query(User).all()

@router.get("/consultations", response_model=list[ConsultationResponse])
def get_all_consultations(db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    return db.query(Consultation).all()
