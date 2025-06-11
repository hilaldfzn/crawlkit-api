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
    verify_ssl: bool
    ssl_cert_path: str
    default_user_agent: str
    max_concurrent_requests: int 
    request_delay: float
    respect_robots: bool
    environment: str
    
    class Config:
        env_file = ".env"

settings = Settings()