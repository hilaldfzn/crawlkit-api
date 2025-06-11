from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from ..database import Base
import datetime

class CrawlJob(Base):
    __tablename__ = "crawl_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    description = Column(Text)
    target_urls = Column(JSON)
    extraction_rules = Column(JSON)
    status = Column(String, default="pending")  # pending, running, completed, failed
    scheduled_at = Column(DateTime)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    user = relationship("User", back_populates="crawl_jobs")
    extracted_data = relationship("ExtractedData", back_populates="crawl_job")

class ExtractedData(Base):
    __tablename__ = "extracted_data"
    
    id = Column(Integer, primary_key=True, index=True)
    crawl_job_id = Column(Integer, ForeignKey("crawl_jobs.id"))
    url = Column(String)
    data = Column(JSON)
    extracted_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    crawl_job = relationship("CrawlJob", back_populates="extracted_data")