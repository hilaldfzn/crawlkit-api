from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class ReportBase(BaseModel):
    title: str
    description: Optional[str] = None
    crawl_job_ids: List[int]

class ReportCreate(ReportBase):
    pass

class Report(ReportBase):
    id: int
    user_id: int
    report_data: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True