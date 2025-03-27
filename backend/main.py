from contextlib import asynccontextmanager
from fastapi import FastAPI
from auth import router as auth_router
from database import init_db
from routes import consultation, progress, recommendations, user
from routes.analysis import router as analysis_router
from routes.testing import router as testing_router
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = FastAPI(title="Aurora AI Skin Analysis API", version="1.0.0")

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# # Initialize the database
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run database initialization only once at startup."""
    init_db()  # Initialize the database
    yield  
    
app.state.lifespan = lifespan


# Testing routes
app.include_router(testing_router, prefix="", tags=["Testing"])

# Other routes
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(analysis_router, prefix="/analysis", tags=["Skin Analysis"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])
app.include_router(progress.router, prefix="/progress", tags=["Progress"])
app.include_router(consultation.router, prefix="/consultations", tags=["Consultations"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),  
        reload=True,  
        log_level="info" 
    )
