from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Select database: PostgreSQL if available, otherwise use SQLite
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    engine = create_engine(DATABASE_URL, echo=True)  # PostgreSQL from env
    logger.info("Using PostgreSQL database.")
else:
    DATABASE_URL = "sqlite:///aurora_ai.db"  # Fallback to SQLite
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)
    logger.info("Using SQLite database (fallback).")

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

# Initialize the database
def init_db():
    logger.info("Initializing database...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully.")
