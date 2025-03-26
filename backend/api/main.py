from fastapi import FastAPI, File, UploadFile, Form, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
import shutil
import os

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:3000",  # Allow frontend running on localhost 
    "http://127.0.0.1:3000",
    "*",  # Allow all origins (use with caution in production)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Database setup
DATABASE_URL = "sqlite:///./skin_analysis.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserSkinData(Base):
    __tablename__ = "user_skin_data"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    skin_conditions = Column(String)  # Comma-separated values

Base.metadata.create_all(bind=engine)

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for response
class SkinConditionsResponse(BaseModel):
    email: str
    skin_conditions: List[str]

@app.post("/upload/")
def upload_image(email: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Save image to a local directory (mocking actual processing)
    image_path = f"uploaded_images/{email}.jpg"
    os.makedirs("uploaded_images", exist_ok=True)
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Mock analysis of skin conditions
    mock_conditions = ["Acne", "Dry Skin", "Hyperpigmentation"]  # Replace with actual ML model analysis
    condition_str = ",".join(mock_conditions)
    
    # Store in database
    user_data = db.query(UserSkinData).filter(UserSkinData.email == email).first()
    if user_data:
        user_data.skin_conditions = condition_str
    else:
        user_data = UserSkinData(email=email, skin_conditions=condition_str)
        db.add(user_data)
    db.commit()
    
    return {"message": "Image received and processed", "email": email, "skin_conditions": mock_conditions}

@app.get("/conditions/{email}", response_model=SkinConditionsResponse)
def get_skin_conditions(email: str, db: Session = Depends(get_db)):
    user_data = db.query(UserSkinData).filter(UserSkinData.email == email).first()
    if not user_data:
        return {"email": email, "skin_conditions": []}
    return {"email": user_data.email, "skin_conditions": user_data.skin_conditions.split(",")}
