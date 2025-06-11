from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.crawl_job import CrawlJob, CrawlJobCreate, CrawlJobUpdate, ExtractedDataResponse
from ..services.crawl_service import CrawlService
from ..dependencies import get_current_active_user
from ..models.user import User
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

def run_crawl_job_sync(job_id: int, db: Session):
    """Background task to run crawl job"""
    crawl_service = CrawlService(db)
    result = crawl_service.execute_crawl_job(job_id)
    logger.info(f"Background crawl job {job_id} completed with result: {result}")

@router.post("/", response_model=CrawlJob)
async def create_crawl_job(
    crawl_job: CrawlJobCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    crawl_service = CrawlService(db)
    job = crawl_service.create_crawl_job(crawl_job, current_user.id)
    
    # Add background task to execute crawl job
    background_tasks.add_task(run_crawl_job_sync, job.id, db)
    
    logger.info(f"Created crawl job {job.id} for user {current_user.id}")
    return job

@router.post("/{job_id}/execute", response_model=dict)
async def execute_crawl_job_now(
    job_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Execute a crawl job immediately (for testing)"""
    crawl_service = CrawlService(db)
    job = crawl_service.get_crawl_job(job_id, current_user.id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Crawl job not found")
    
    if job.status == "running":
        raise HTTPException(status_code=400, detail="Job is already running")
    
    success = crawl_service.execute_crawl_job(job_id)
    
    return {
        "message": "Job execution completed",
        "success": success,
        "job_id": job_id
    }

@router.get("/", response_model=List[CrawlJob])
async def get_crawl_jobs(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    crawl_service = CrawlService(db)
    jobs = crawl_service.get_crawl_jobs(current_user.id, skip, limit)
    logger.info(f"Retrieved {len(jobs)} crawl jobs for user {current_user.id}")
    return jobs

@router.get("/{job_id}", response_model=CrawlJob)
async def get_crawl_job(
    job_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    crawl_service = CrawlService(db)
    job = crawl_service.get_crawl_job(job_id, current_user.id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Crawl job not found")
    
    return job

@router.put("/{job_id}", response_model=CrawlJob)
async def update_crawl_job(
    job_id: int,
    job_update: CrawlJobUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    crawl_service = CrawlService(db)
    job = crawl_service.update_crawl_job(job_id, current_user.id, job_update)
    
    if not job:
        raise HTTPException(status_code=404, detail="Crawl job not found")
    
    logger.info(f"Updated crawl job {job_id}")
    return job

@router.delete("/{job_id}")
async def delete_crawl_job(
    job_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    crawl_service = CrawlService(db)
    if not crawl_service.delete_crawl_job(job_id, current_user.id):
        raise HTTPException(status_code=404, detail="Crawl job not found")
    
    logger.info(f"Deleted crawl job {job_id}")
    return {"message": "Crawl job deleted successfully"}

@router.get("/{job_id}/data", response_model=List[ExtractedDataResponse])
async def get_extracted_data(
    job_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    crawl_service = CrawlService(db)
    data = crawl_service.get_extracted_data(job_id, current_user.id)
    logger.info(f"Retrieved {len(data)} extracted records for job {job_id}")
    return data

@router.get("/{job_id}/status")
async def get_crawl_job_status(
    job_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    crawl_service = CrawlService(db)
    job = crawl_service.get_crawl_job(job_id, current_user.id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Crawl job not found")
    
    return {
        "id": job.id,
        "name": job.name,
        "status": job.status,
        "started_at": job.started_at,
        "completed_at": job.completed_at,
        "created_at": job.created_at,
        "updated_at": job.updated_at
    }