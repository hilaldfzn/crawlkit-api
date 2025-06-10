from pydantic import BaseModel, validator
from typing import List, Dict, Any, Optional
from datetime import datetime

class CrawlJobBase(BaseModel):
    name: str
    description: Optional[str] = None
    target_urls: List[str]
    extraction_rules: Dict[str, str]
    scheduled_at: Optional[datetime] = None

class CrawlJobCreate(CrawlJobBase):
    @validator('target_urls')
    def validate_urls(cls, v):
        if not v:
            raise ValueError('At least one URL is required')
        return v

class CrawlJobUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    target_urls: Optional[List[str]] = None
    extraction_rules: Optional[Dict[str, str]] = None
    scheduled_at: Optional[datetime] = None

class CrawlJob(CrawlJobBase):
    id: int
    user_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ExtractedDataResponse(BaseModel):
    id: int
    url: str
    data: Dict[str, Any]
    extracted_at: datetime
    
    class Config:
        from_attributes = True