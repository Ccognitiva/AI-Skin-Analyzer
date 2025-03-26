from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models import SkinAnalysis
from schemas import AnalysisResult
import shutil

router = APIRouter()

@router.post("/analyze-skin", response_model=AnalysisResult)
async def analyze_skin(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_location = f"uploads/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Simulate AI Model (Replace with actual model logic)
    detected_conditions = ["Acne, Dryness"]  
    new_analysis = SkinAnalysis(image_url=file_location, detected_conditions=detected_conditions)
    
    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)
    return new_analysis
