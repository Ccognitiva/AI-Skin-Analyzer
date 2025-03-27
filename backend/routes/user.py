from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User
from schemas import UserListResponse, UserResponse
from database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


# Get a user by ID route
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Get all users route
@router.get("/", response_model=UserListResponse)
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"users": users}