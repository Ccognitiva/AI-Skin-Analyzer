from pydantic import BaseModel
from datetime import datetime
from typing import List

class ConditionResponse(BaseModel):
    condition_id: int
    name: str

    class Config:
        from_attributes = True  # Allows SQLAlchemy-to-Pydantic conversion

class AnalysisResult(BaseModel):
    analysis_id: int
    user_id: int
    image_url: str
    detected_conditions: List[ConditionResponse]
    analysis_date: datetime

    class Config:
        from_attributes = True
        

# Schema for creating a new user
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    skin_type: str = None  # Optional field for skin type

    class Config:
        orm_mode = True  # To allow SQLAlchemy model conversion

# Schema for user response (for returning user details)
class UserResponse(BaseModel):
    user_id: int
    name: str
    email: str
    skin_type: str
    created_at: str

    class Config:
        orm_mode = True

# Schema for a list of users response
class UserListResponse(BaseModel):
    users: List[UserResponse]


class LoginRequest(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True