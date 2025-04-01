import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import OperationalError
import time

# Database connection parameters from environment variables
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME', 'newsdb')
DB_USER = os.environ.get('DB_USER', 'devuser')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'devpassword')

# Create the database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def get_engine(retries=5, delay=5):
    """Create database engine with connection retry logic"""
    for attempt in range(retries):
        try:
            engine = create_engine(
                DATABASE_URL,
                echo=True
            )
            
            # Test the connection
            connection = engine.connect()
            connection.close()
            
            return engine
        
        except OperationalError as e:
            if attempt < retries - 1:
                print(f"Database connection failed (attempt {attempt+1}/{retries}): {e}")
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"Database connection failed after {retries} attempts: {e}")
                raise


def init_db():
    """Initialize the database schema"""
    from models import Base
    Base.metadata.create_all(get_engine())
    print("Database initialized successfully.")