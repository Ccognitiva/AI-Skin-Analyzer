from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

# Condition Response Schema
class ConditionResponse(BaseModel):
    condition_id: int
    name: str

    class Config:
        from_attributes = True  # Enables SQLAlchemy-to-Pydantic conversion

# Analysis Result Schema
class AnalysisResult(BaseModel):
    analysis_id: int
    user_id: int
    image_url: str
    detected_conditions: List[ConditionResponse]
    analysis_date: datetime

    class Config:
        from_attributes = True

# User Creation Schema
class UserCreate(BaseModel):
    name: str
    email: EmailStr  
    password: str
    skin_type: Optional[str] = None  

    class Config:
        from_attributes = True

# User Response Schema
class UserResponse(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    skin_type: Optional[str]
    created_at: datetime 

    class Config:
        from_attributes = True

# List of Users Response Schema
class UserListResponse(BaseModel):
    users: List[UserResponse]

# Login Request Schema
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True

# Login Response Schema
class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    skin_type: Optional[str] = None

    class Config:
        from_attributes = True