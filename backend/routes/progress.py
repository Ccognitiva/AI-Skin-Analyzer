from fastapi import APIRouter


router = APIRouter(prefix="/progress", tags=["Progress"])

@router.post("/")
def add_progress():
    pass

@router.get("/")
def get_progress():
    pass
