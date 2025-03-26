from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models import User
from database import get_db
from security import verify_token  # You can implement this for token verification

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency for getting the current authenticated user
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_token(token)
        user = db.query(User).filter(User.id == payload["sub"]).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# Dependency for getting the current authenticated admin user
def get_admin_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_token(token)
        user = db.query(User).filter(User.id == payload["sub"]).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        if not user.is_admin:  # Assuming you have a field like is_admin in the User model
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
