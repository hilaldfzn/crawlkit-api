from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging
import datetime

from .api import auth, users, crawl_jobs, reports
from .database import engine
from .models import user, crawl_job, report

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables
user.Base.metadata.create_all(bind=engine)
crawl_job.Base.metadata.create_all(bind=engine)
report.Base.metadata.create_all(bind=engine)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Advanced Web Crawler API",
    description="A powerful web crawling API with data extraction and analytics capabilities",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(crawl_jobs.router, prefix="/crawl-jobs", tags=["Crawl Jobs"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])

@app.get("/")
@limiter.limit("10/minute")
async def root(request: Request):
    return {
        "message": "Advanced Web Crawler API",
        "version": "1.0.0",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

@app.get("/health")
@limiter.limit("30/minute")
async def health_check(request: Request):
    return {
        "status": "healthy",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )