# Web Crawler API - Complete Documentation

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [System Requirements](#system-requirements)
4. [Installation & Setup](#installation--setup)
5. [Project Structure](#project-structure)
6. [Configuration](#configuration)
7. [Running the Application](#running-the-application)
8. [API Documentation](#api-documentation)
9. [Usage Examples](#usage-examples)
10. [Testing](#testing)
11. [Deployment](#deployment)
12. [Troubleshooting](#troubleshooting)
13. [Contributing](#contributing)

## 🌟 Project Overview

The Web Crawler API is a powerful, scalable web scraping solution built with FastAPI. It provides comprehensive data extraction, analytics, and reporting capabilities with a focus on ethical crawling practices and robust security.

### Key Capabilities
- **Intelligent Web Crawling** with robots.txt compliance
- **Data Extraction** using CSS selectors
- **User Management** with JWT authentication
- **Background Job Processing** for large-scale operations
- **Analytics & Reporting** with data insights
- **Rate Limiting** and security measures
- **RESTful API** with automatic documentation

## ✨ Features

### Core Features
- ✅ **RESTful API** with FastAPI and automatic OpenAPI documentation
- ✅ **Advanced Web Crawling** with async processing and robots.txt compliance
- ✅ **Flexible Data Extraction** using CSS selectors
- ✅ **User Authentication** with JWT tokens and password hashing
- ✅ **Background Job Processing** with Celery and Redis
- ✅ **Analytics Dashboard** with success rates and data insights
- ✅ **Rate Limiting** to prevent abuse
- ✅ **Docker Support** for easy deployment
- ✅ **Comprehensive Testing** with pytest

### Security Features
- 🔐 **JWT Authentication** with secure token handling
- 🔐 **Password Hashing** using bcrypt
- 🔐 **Input Validation** and sanitization
- 🔐 **CORS Configuration** for cross-origin requests
- 🔐 **Rate Limiting** with configurable thresholds

### Crawling Features
- 🕷️ **Robots.txt Compliance** for ethical crawling
- 🕷️ **Concurrent Processing** with configurable limits
- 🕷️ **Request Delays** to respect server resources
- 🕷️ **Error Handling** with retry mechanisms
- 🕷️ **User-Agent Rotation** for better success rates

## 🖥️ System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **Database**: PostgreSQL 12+
- **Cache**: Redis 6+
- **Memory**: 2GB RAM
- **Storage**: 5GB available space

### Recommended Requirements
- **Python**: 3.11+
- **Database**: PostgreSQL 15+
- **Cache**: Redis 7+
- **Memory**: 4GB RAM
- **Storage**: 20GB available space

### Development Tools
- **Git**: For version control
- **Docker**: For containerized deployment (optional)
- **VS Code/PyCharm**: Recommended IDEs

## 🚀 Installation & Setup

### Method 1: Local Development Setup

#### Step 1: Clone the Repository
```bash
# Clone the repository
git clone <repository-url>
cd web-crawler-api

# Verify project structure
ls -la
```

#### Step 2: Set Up Python Environment
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Verify Python version
python --version  # Should be 3.8+
```

#### Step 3: Install Dependencies
```bash
# Install Python packages
pip install --upgrade pip
pip install -r requirements.txt

# Verify installation
pip list
```

#### Step 4: Database Setup
```bash
# Install PostgreSQL (if not already installed)
# On Ubuntu/Debian:
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# On macOS (using Homebrew):
brew install postgresql
brew services start postgresql

# On Windows: Download from postgresql.org

# Create database
sudo -u postgres createdb webcrawler
sudo -u postgres createuser --interactive  # Create user with password
```

#### Step 5: Redis Setup
```bash
# Install Redis (if not already installed)
# On Ubuntu/Debian:
sudo apt-get install redis-server

# On macOS (using Homebrew):
brew install redis
brew services start redis

# On Windows: Download from redis.io

# Test Redis connection
redis-cli ping  # Should return PONG
```

#### Step 6: Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env  # or use your preferred editor
```

**Required Environment Variables:**
```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/webcrawler
TEST_DATABASE_URL=postgresql://username:password@localhost:5432/webcrawler_test

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Email Configuration (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600

# Crawler Settings
DEFAULT_USER_AGENT=AdvancedWebCrawler/1.0
MAX_CONCURRENT_REQUESTS=10
REQUEST_DELAY=1.0

# Environment
ENVIRONMENT=development
```

#### Step 8: Initialize Database
```bash
# Navigate back to project root
cd ..

# Run database setup script
python scripts/setup_database.py

# Seed sample data (optional)
python scripts/seed_data.py
```

### Method 2: Docker Setup

#### Step 1: Install Docker
```bash
# Install Docker and Docker Compose
# On Ubuntu:
sudo apt-get update
sudo apt-get install docker.io docker-compose

# On macOS: Install Docker Desktop
# On Windows: Install Docker Desktop

# Verify installation
docker --version
docker-compose --version
```

#### Step 2: Run with Docker Compose
```bash
# Clone repository
git clone <repository-url>
cd web-crawler-api

# Start all services
docker-compose up --build

# Run in background (detached mode)
docker-compose up -d --build
```

#### Step 3: Verify Docker Setup
```bash
# Check running containers
docker-compose ps

# View logs
docker-compose logs backend
docker-compose logs db
docker-compose logs redis

# Access container shell
docker-compose exec backend bash
```

## 📁 Project Structure

```
web-crawler-api/
├── backend/                          # Backend application
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI application entry point
│   │   ├── config.py                 # Configuration settings
│   │   ├── database.py               # Database connection and setup
│   │   ├── dependencies.py           # Common dependencies
│   │   ├── models/                   # Database models
│   │   │   ├── __init__.py
│   │   │   ├── user.py              # User database model
│   │   │   ├── crawl_job.py         # Crawl job database model
│   │   │   └── report.py            # Report database model
│   │   ├── schemas/                 # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py              # User Pydantic schemas
│   │   │   ├── crawl_job.py         # Crawl job Pydantic schemas
│   │   │   └── report.py            # Report Pydantic schemas
│   │   ├── api/                     # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── auth.py              # Authentication endpoints
│   │   │   ├── users.py             # User management endpoints
│   │   │   ├── crawl_jobs.py        # Crawl job endpoints
│   │   │   └── reports.py           # Report endpoints
│   │   ├── core/                    # Core functionality
│   │   │   ├── __init__.py
│   │   │   ├── security.py          # Password hashing, JWT tokens
│   │   │   ├── crawler.py           # Main crawler implementation
│   │   │   ├── data_extractor.py    # Data extraction logic
│   │   │   └── robots_checker.py    # Robots.txt validation
│   │   ├── services/                # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── user_service.py      # User business logic
│   │   │   ├── crawl_service.py     # Crawl job business logic
│   │   │   └── report_service.py    # Report business logic
│   │   └── utils/                   # Utility functions
│   │       ├── __init__.py
│   │       ├── validators.py        # Input validation
│   │       └── helpers.py           # Utility functions
│   ├── requirements.txt             # Python dependencies
│   ├── Dockerfile                   # Docker configuration
│   └── docker-compose.yml          # Local Docker setup
├── tests/                           # Test suite
│   ├── test_auth.py                # Authentication tests
│   ├── test_crawl_jobs.py          # Crawl job tests
│   └── test_crawler.py             # Crawler tests
├── docs/                           # Documentation
│   ├── api_documentation.md        # API documentation
│   └── user_guide.md              # User guide
├── scripts/                        # Utility scripts
│   ├── setup_database.py          # Database setup
│   └── seed_data.py               # Sample data
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
├── README.md                       # Project README
└── docker-compose.yml             # Production Docker setup
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/webcrawler
TEST_DATABASE_URL=postgresql://username:password@localhost:5432/webcrawler_test

# Security Settings
SECRET_KEY=your-super-secret-key-change-this-in-production-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Email Settings (Optional for notifications)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600

# Crawler Settings
DEFAULT_USER_AGENT=AdvancedWebCrawler/1.0
MAX_CONCURRENT_REQUESTS=10
REQUEST_DELAY=1.0

# Application Environment
ENVIRONMENT=development
```

### Database Configuration

For production, use a robust PostgreSQL setup:

```sql
-- Create database and user
CREATE DATABASE webcrawler;
CREATE USER webcrawler_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE webcrawler TO webcrawler_user;

-- Create test database
CREATE DATABASE webcrawler_test;
GRANT ALL PRIVILEGES ON DATABASE webcrawler_test TO webcrawler_user;
```

### Redis Configuration

For production Redis setup:

```conf
# redis.conf
bind 127.0.0.1
port 6379
requirepass your_redis_password
maxmemory 256mb
maxmemory-policy allkeys-lru
```

## 🏃‍♂️ Running the Application

### Development Mode

#### Method 1: Direct Python
```bash
# Navigate to backend directory
cd backend

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Alternative with auto-reload
python -m uvicorn app.main:app --reload
```

#### Method 2: With Environment Variables
```bash
# Set environment variables
export DATABASE_URL="postgresql://user:pass@localhost:5432/webcrawler"
export REDIS_URL="redis://localhost:6379"
export SECRET_KEY="your-secret-key"

# Run application
uvicorn app.main:app --reload
```

#### Method 3: Using Python Script
```python
# run.py
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
```

```bash
python run.py
```

### Production Mode

#### Method 1: Gunicorn
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### Method 2: Docker Production
```bash
# Build production image
docker build -t web-crawler-api .

# Run production container
docker run -d \
  --name web-crawler-api \
  -p 8000:8000 \
  --env-file .env \
  web-crawler-api
```

#### Method 3: Docker Compose Production
```bash
# Use production compose file
docker-compose -f docker-compose.prod.yml up -d
```

### Background Worker (Celery)

```bash
# Terminal 1: Start Celery worker
cd backend
celery -A app.worker worker --loglevel=info

# Terminal 2: Start Celery beat (for scheduled tasks)
celery -A app.worker beat --loglevel=info

# Terminal 3: Monitor Celery (optional)
celery -A app.worker flower
```

### Verify Installation

1. **Check API Health:**
```bash
curl http://localhost:8000/health
```

2. **Access API Documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. **Test Database Connection:**
```bash
# In Python shell
python -c "
from backend.app.database import engine
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(text('SELECT 1'))
    print('Database connected:', result.fetchone())
"
```

4. **Test Redis Connection:**
```bash
redis-cli ping
```

## 📖 API Documentation

For API Documentation, visit the link [here](https://github.com/hilaldfzn/crawlkit-api/blob/main/docs/api_documentation.md).

## 💡 Usage Examples
For a usage tutorial, visit the link [here](https://github.com/hilaldfzn/crawlkit-api/blob/main/docs/user_guide.md).

## 🧪 Testing

### Running Tests

#### Unit Tests
```bash
# Navigate to backend directory
cd backend

# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_auth.py -v

# Run with coverage report
pytest tests/ --cov=app --cov-report=html --cov-report=term

# Run tests with detailed output
pytest tests/ -v -s
```

#### Integration Tests
```bash
# Test API endpoints
pytest tests/test_api/ -v

# Test crawler functionality
pytest tests/test_crawler.py -v

# Test database operations
pytest tests/test_database.py -v
```

### Sample Test Cases

```python
# tests/test_crawl_jobs.py
def test_create_crawl_job(authenticated_client):
    """Test creating a new crawl job"""
    job_data = {
        "name": "Test Crawler",
        "target_urls": ["https://httpbin.org/html"],
        "extraction_rules": {
            "title": "title",
            "heading": "h1"
        }
    }
    
    response = authenticated_client.post("/crawl-jobs/", json=job_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == "Test Crawler"
    assert data["status"] == "pending"
    assert "id" in data

def test_list_crawl_jobs(authenticated_client):
    """Test listing crawl jobs"""
    response = authenticated_client.get("/crawl-jobs/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_get_crawl_job_status(authenticated_client):
    """Test getting crawl job status"""
    # Create job first
    job_data = {
        "name": "Status Test",
        "target_urls": ["https://httpbin.org/html"],
        "extraction_rules": {"title": "title"}
    }
    create_response = authenticated_client.post("/crawl-jobs/", json=job_data)
    job_id = create_response.json()["id"]
    
    # Get status
    response = authenticated_client.get(f"/crawl-jobs/{job_id}/status")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert data["id"] == job_id
```

#### Documentation Standards
- Use clear, descriptive docstrings
- Include type hints for all functions
- Add comments for complex logic
- Update API documentation for new endpoints

### Testing Requirements
- Write unit tests for new features
- Ensure 80%+ code coverage
- Test error handling scenarios
- Include integration tests for API endpoints

## 🙏 Acknowledgments

- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - Python SQL toolkit and ORM
- **BeautifulSoup** - Python library for parsing HTML and XML
- **Celery** - Distributed task queue for Python
- **PostgreSQL** - Advanced open source relational database
- **Redis** - In-memory data structure store
- **Docker** - Platform for developing, shipping, and running applications

---

**Happy Crawling! 🕷️**

For more information, visit the [API documentation](http://localhost:8000/docs) when running the application.