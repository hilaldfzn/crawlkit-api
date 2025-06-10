import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from backend.app.database import Base
from backend.app.models import user, crawl_job, report
from backend.app.config import settings

def create_tables():
    """Create all database tables"""
    engine = create_engine(settings.database_url)
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_tables()