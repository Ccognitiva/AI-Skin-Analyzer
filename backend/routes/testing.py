from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    """Health check to verify the server is running."""
    return {"status": "success", "message": "Server is running smoothly!"}

@router.get("/")
def root():
    """Root route for a welcome message."""
    return {"message": "Welcome to the Aurora AI Skincare Analysis API!"}
