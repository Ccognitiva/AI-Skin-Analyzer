from fastapi import APIRouter


router = APIRouter()

@router.post("/")
def add_progress():
    pass

@router.get("/")
def get_progress():
    pass
