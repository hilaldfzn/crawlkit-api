from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.main import app
from backend.app.database import get_db, Base

# Test database setup (same as test_auth.py)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def get_auth_token():
    # Create user and get token
    client.post(
        "/auth/signup",
        json={
            "email": "testuser@example.com",
            "password": "testpassword",
            "full_name": "Test User"
        }
    )
    
    response = client.post(
        "/auth/login",
        data={
            "username": "testuser@example.com",
            "password": "testpassword"
        }
    )
    return response.json()["access_token"]

def test_create_crawl_job():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    crawl_job_data = {
        "name": "Test Crawl Job",
        "description": "A test crawl job",
        "target_urls": ["https://example.com"],
        "extraction_rules": {
            "title": "title",
            "heading": "h1"
        }
    }
    
    response = client.post("/crawl-jobs/", json=crawl_job_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Crawl Job"
    assert "id" in data

def test_get_crawl_jobs():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/crawl-jobs/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)