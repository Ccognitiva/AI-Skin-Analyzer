from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models import SkinAnalysis, SkinCondition, skin_analysis_conditions, User
from schemas import AnalysisResult, ConditionResponse
import shutil
import os
import uuid
from datetime import datetime

router = APIRouter()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure uploads folder exists

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/jpg"}

@router.post("/analyze-skin", response_model=AnalysisResult)
async def analyze_skin(
    file: UploadFile = File(...),
    user_id: int = None,  
    db: Session = Depends(get_db)
):
    """Handles skin analysis image uploads and links detected skin conditions to the user."""

    # Validate user
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Validate file type
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid image format. Only JPEG and PNG are allowed.")

    # Generate a secure filename
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_location = os.path.join(UPLOAD_FOLDER, unique_filename)

    # Save image
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
    new_analysis = SkinAnalysis(user_id=user_id, image_url=file_location, analysis_date=datetime.now(datetime.timezone.utc)
)
    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)

    # Link detected conditions to the analysis
    for condition in detected_conditions:
        db.execute(
            skin_analysis_conditions.insert().values(
                analysis_id=new_analysis.analysis_id,
                condition_id=condition.condition_id
            )
        )
    
    db.commit()

    # Return structured response using Pydantic
    return AnalysisResult(
        analysis_id=new_analysis.analysis_id,
        user_id=new_analysis.user_id,
        image_url=new_analysis.image_url,
        detected_conditions=[ConditionResponse(condition_id=c.condition_id, name=c.name) for c in detected_conditions],
        analysis_date=new_analysis.analysis_date
    )
