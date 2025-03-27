from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Select database: PostgreSQL if available, otherwise use SQLite
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    engine = create_engine(DATABASE_URL)  # Use PostgreSQL from env
else:
    DATABASE_URL = "sqlite:///aurora_ai.db"  # Fallback to SQLite
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session and base class
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
