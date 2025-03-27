from fastapi import APIRouter

router = APIRouter(prefix="/consultation", tags=["Consultation"])

@router.post("/")
def book_consultation():
    pass

@router.get("/")
def get_consultations():
    pass
