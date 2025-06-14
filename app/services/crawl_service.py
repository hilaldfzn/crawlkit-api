from sqlalchemy.orm import Session
from ..models.crawl_job import CrawlJob, ExtractedData
from ..schemas.crawl_job import CrawlJobCreate, CrawlJobUpdate
from ..core.crawler import SimpleCrawler
from typing import Dict, List, Optional
import asyncio
import logging
import datetime

logger = logging.getLogger(__name__)

class CrawlService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_crawl_job(self, crawl_job: CrawlJobCreate, user_id: int) -> CrawlJob:
        db_crawl_job = CrawlJob(
            user_id=user_id,
            name=crawl_job.name,
            description=crawl_job.description,
            target_urls=crawl_job.target_urls,
            extraction_rules=crawl_job.extraction_rules,
            scheduled_at=crawl_job.scheduled_at
        )
        self.db.add(db_crawl_job)
        self.db.commit()
        self.db.refresh(db_crawl_job)
        return db_crawl_job
    
    def get_crawl_jobs(self, user_id: int, skip: int = 0, limit: int = 100) -> List[CrawlJob]:
        return self.db.query(CrawlJob).filter(
            CrawlJob.user_id == user_id
        ).offset(skip).limit(limit).all()
    
    def get_crawl_job(self, job_id: int, user_id: int) -> Optional[CrawlJob]:
        return self.db.query(CrawlJob).filter(
            CrawlJob.id == job_id,
            CrawlJob.user_id == user_id
        ).first()
    
    def update_crawl_job(self, job_id: int, user_id: int, job_update: CrawlJobUpdate) -> Optional[CrawlJob]:
        job = self.get_crawl_job(job_id, user_id)
        if not job:
            return None
        
        update_data = job_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(job, field, value)
        
        job.updated_at = datetime.datetime.utcnow()
        self.db.commit()
        self.db.refresh(job)
        return job
    
    def delete_crawl_job(self, job_id: int, user_id: int) -> bool:
        job = self.get_crawl_job(job_id, user_id)
        if not job:
            return False
        
        # Delete associated extracted data
        self.db.query(ExtractedData).filter(
            ExtractedData.crawl_job_id == job_id
        ).delete()
        
        self.db.delete(job)
        self.db.commit()
        return True
    
    def execute_crawl_job(self, job_id: int) -> bool:
        """Execute a crawl job synchronously"""
        job = self.db.query(CrawlJob).filter(CrawlJob.id == job_id).first()
        if not job:
            logger.error(f"Crawl job {job_id} not found")
            return False
        
        try:
            # Update job status
            job.status = "running"
            job.started_at = datetime.datetime.utcnow()
            self.db.commit()
            
            logger.info(f"Starting crawl job {job_id}: {job.name}")
            
            # Execute crawling synchronously
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                results = loop.run_until_complete(self._run_crawler(job))
            finally:
                loop.close()
            
            # Store extracted data
            for result in results:
                extracted_data = ExtractedData(
                    crawl_job_id=job.id,
                    url=result["url"],
                    data=result.get("data", {})
                )
                self.db.add(extracted_data)
            
            # Update job status
            job.status = "completed"
            job.completed_at = datetime.datetime.utcnow()
            self.db.commit()
            
            logger.info(f"Crawl job {job_id} completed successfully. Extracted {len(results)} records.")
            return True
            
        except Exception as e:
            job.status = "failed"
            job.completed_at = datetime.datetime.utcnow()
            self.db.commit()
            
            logger.error(f"Crawl job {job_id} failed: {e}")
            return False
    
    async def _run_crawler(self, job: CrawlJob) -> List[Dict]:
        """Run the crawler asynchronously"""
        async with SimpleCrawler(
            max_concurrent=3,  # Conservative for local development
            delay_range=(1, 2),
            respect_robots=True,
            verify_ssl=True
        ) as crawler:
            return await crawler.crawl_urls(job.target_urls, job.extraction_rules)
    
    def get_extracted_data(self, job_id: int, user_id: int) -> List[ExtractedData]:
        job = self.get_crawl_job(job_id, user_id)
        if not job:
            return []
        
        return self.db.query(ExtractedData).filter(
            ExtractedData.crawl_job_id == job_id
        ).all()