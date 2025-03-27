from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models import SkinAnalysis, SkinCondition, skin_analysis_conditions, User
from schemas import AnalysisResult
import shutil
import os

router = APIRouter()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure uploads folder exists

@router.post("/analyze-skin", response_model=AnalysisResult)
async def analyze_skin(
    file: UploadFile = File(...), 
    user_id: int = None,  # Accepts a user ID
    db: Session = Depends(get_db)
):
    # Validate user
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Save image
    file_location = f"{UPLOAD_FOLDER}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Simulate AI Model (Replace with actual AI inference)
    detected_condition_names = ["Acne", "Dryness"]  

    # Retrieve or create detected skin conditions
    detected_conditions = []
    for condition_name in detected_condition_names:
        condition = db.query(SkinCondition).filter(SkinCondition.name == condition_name).first()
        if not condition:
            condition = SkinCondition(name=condition_name, description=f"{condition_name} detected")
            db.add(condition)
            db.commit()
            db.refresh(condition)
        detected_conditions.append(condition)

    # Create new SkinAnalysis entry
    new_analysis = SkinAnalysis(user_id=user_id, image_url=file_location)
    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)

    # Link detected conditions to the analysis
    for condition in detected_conditions:
        stmt = skin_analysis_conditions.insert().values(analysis_id=new_analysis.analysis_id, condition_id=condition.condition_id)
        db.execute(stmt)
    
    db.commit()

    # Return structured response
    return {
        "analysis_id": new_analysis.analysis_id,
        "user_id": new_analysis.user_id,
        "image_url": new_analysis.image_url,
        "detected_conditions": [{"condition_id": c.condition_id, "name": c.name} for c in detected_conditions],
        "analysis_date": new_analysis.analysis_date
    }
