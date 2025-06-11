from sqlalchemy.orm import Session
from ..models.report import Report
from ..models.crawl_job import ExtractedData
from ..schemas.report import ReportCreate
from typing import List, Optional, Dict, Any

class ReportService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_report(self, report: ReportCreate, user_id: int) -> Report:
        report_data = self._generate_report_data(report.crawl_job_ids, user_id)
        
        db_report = Report(
            user_id=user_id,
            title=report.title,
            description=report.description,
            crawl_job_ids=report.crawl_job_ids,
            report_data=report_data
        )
        self.db.add(db_report)
        self.db.commit()
        self.db.refresh(db_report)
        return db_report
    
    def get_reports(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Report]:
        return self.db.query(Report).filter(
            Report.user_id == user_id
        ).offset(skip).limit(limit).all()
    
    def get_report(self, report_id: int, user_id: int) -> Optional[Report]:
        return self.db.query(Report).filter(
            Report.id == report_id,
            Report.user_id == user_id
        ).first()
    
    def _generate_report_data(self, crawl_job_ids: List[int], user_id: int) -> Dict[str, Any]:
        """Generate analytics and insights from crawl job data"""
        report_data = {
            "total_jobs": len(crawl_job_ids),
            "total_urls_crawled": 0,
            "successful_extractions": 0,
            "failed_extractions": 0,
            "data_summary": {},
            "common_fields": []
        }
        
        all_data = []
        field_counts = {}
        
        for job_id in crawl_job_ids:
            extracted_data = self.db.query(ExtractedData).filter(
                ExtractedData.crawl_job_id == job_id
            ).all()
            
            for data in extracted_data:
                report_data["total_urls_crawled"] += 1
                
                if data.data and not data.data.get("error"):
                    report_data["successful_extractions"] += 1
                    all_data.append(data.data)
                    
                    for field in data.data.keys():
                        field_counts[field] = field_counts.get(field, 0) + 1
                else:
                    report_data["failed_extractions"] += 1
        
        if field_counts:
            total_records = len(all_data)
            report_data["common_fields"] = [
                field for field, count in field_counts.items()
                if count >= total_records * 0.5
            ]
        
        report_data["data_summary"] = {
            "total_records": len(all_data),
            "field_distribution": field_counts,
            "success_rate": (
                report_data["successful_extractions"] / report_data["total_urls_crawled"]
                if report_data["total_urls_crawled"] > 0 else 0
            )
        }
        
        return report_data