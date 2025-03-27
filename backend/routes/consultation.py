from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def book_consultation():
    pass

@router.get("/")
def get_consultations():
    pass
