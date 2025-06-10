import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from backend.app.models.user import User
from backend.app.models.crawl_job import CrawlJob
from backend.app.core.security import get_password_hash
from backend.app.config import settings

def seed_data():
    """Seed the database with sample data"""
    engine = create_engine(settings.database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Create sample user
        if not db.query(User).filter(User.email == "admin@example.com").first():
            admin_user = User(
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),
                full_name="Admin User",
                is_verified=True
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            
            # Create sample crawl job
            sample_job = CrawlJob(
                user_id=admin_user.id,
                name="Sample News Crawler",
                description="A sample crawl job for news websites",
                target_urls=["https://example.com/news"],
                extraction_rules={
                    "title": "h1",
                    "content": ".article-content",
                    "author": ".author"
                }
            )
            db.add(sample_job)
            db.commit()
            
            print("Sample data created successfully!")
        else:
            print("Sample data already exists!")
            
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()