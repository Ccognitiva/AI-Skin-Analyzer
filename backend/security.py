import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException

# Secret key for encoding and decoding JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # You can add extra checks, like checking expiration or other claims
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
