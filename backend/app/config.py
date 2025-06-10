from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://hilaldfzn@localhost/webcrawler"
    test_database_url: str = "postgresql://hilaldfzn@localhost/webcrawler_test"
    
    # Security
    secret_key: str = "_G1EDD9dsf6fWqVPUDZ_a3VvmzoP1a5o6C5UkvpJLoQ"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # Email
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    
    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 3600
    
    # Crawler Settings
    default_user_agent: str = "AdvancedWebCrawler/1.0"
    max_concurrent_requests: int = 10
    request_delay: float = 1.0

    # Environment
    environment: str = "development"
    
    class Config:
        env_file = ".env"

settings = Settings()