from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.report import Report, ReportCreate
from ..services.report_service import ReportService
from ..dependencies import get_current_active_user
from ..models.user import User

router = APIRouter()

@router.post("/", response_model=Report)
async def create_report(
    report: ReportCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    report_service = ReportService(db)
    return report_service.create_report(report, current_user.id)

@router.get("/", response_model=List[Report])
async def get_reports(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    report_service = ReportService(db)
    return report_service.get_reports(current_user.id, skip, limit)

@router.get("/{report_id}", response_model=Report)
async def get_report(
    report_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    report_service = ReportService(db)
    report = report_service.get_report(report_id, current_user.id)
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return report