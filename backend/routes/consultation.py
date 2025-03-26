from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Consultation
from schemas import ConsultationCreate, ConsultationResponse
from database import get_db
from dependencies import get_current_user

router = APIRouter(prefix="/consultation", tags=["Consultation"])

@router.post("/", response_model=ConsultationResponse)
def book_consultation(consultation: ConsultationCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    new_consultation = Consultation(user_id=user.id, date=consultation.date, status="Pending")
    db.add(new_consultation)
    db.commit()
    db.refresh(new_consultation)
    return new_consultation

@router.get("/", response_model=list[ConsultationResponse])
def get_consultations(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Consultation).filter(Consultation.user_id == user.id).all()
