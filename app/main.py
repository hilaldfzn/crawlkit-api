from http.client import HTTPException
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging
import datetime

from .api import auth, users, crawl_jobs, reports
from .database import create_tables
from .config import settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create tables on startup
create_tables()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["1000/hour"]
)

app = FastAPI(
    title="Web Crawler API - Local Development",
    description="A powerful web crawling API for local development and testing",
    version="1.0.0-dev",
    docs_url="/docs",
    redoc_url="/redoc",
    debug=settings.debug
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
async def root():
    return {
        "message": "Web Crawler API - Local Development",
        "version": "1.0.0-dev",
        "environment": settings.environment,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.environment,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

@app.get("/debug/info")
async def debug_info():
    """Debug endpoint for local development"""
    if settings.environment != "development":
        raise HTTPException(status_code=404, detail="Not found")
    
    return {
        "database_url": settings.database_url.split("://")[0] + "://***",
        "secret_key_set": bool(settings.secret_key),
        "debug_mode": settings.debug,
        "rate_limit": f"{settings.rate_limit_requests}/{settings.rate_limit_window}s"
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}")
    if settings.debug:
        import traceback
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error",
                "error": str(exc),
                "traceback": traceback.format_exc() if settings.debug else None
            }
        )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )