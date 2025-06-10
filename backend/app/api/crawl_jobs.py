from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.crawl_job import CrawlJob, CrawlJobCreate, CrawlJobUpdate, ExtractedDataResponse
from ..services.crawl_service import CrawlService
from ..dependencies import get_current_active_user
from ..models.user import User

router = APIRouter()

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
    background_tasks.add_task(crawl_service.execute_crawl_job, job.id)
    
    return job

@router.get("/", response_model=List[CrawlJob])
async def get_crawl_jobs(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    crawl_service = CrawlService(db)
    return crawl_service.get_crawl_jobs(current_user.id, skip, limit)

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
    
    return {"message": "Crawl job deleted successfully"}

@router.get("/{job_id}/data", response_model=List[ExtractedDataResponse])
async def get_extracted_data(
    job_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    crawl_service = CrawlService(db)
    data = crawl_service.get_extracted_data(job_id, current_user.id)
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
        "status": job.status,
        "started_at": job.started_at,
        "completed_at": job.completed_at
    }