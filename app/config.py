import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    test_database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    rate_limit_requests: int
    rate_limit_window: int
    debug: bool
    default_user_agent: str
    max_concurrent_requests: int 
    request_delay: float
    environment: str
    
    class Config:
        env_file = ".env"

settings = Settings()