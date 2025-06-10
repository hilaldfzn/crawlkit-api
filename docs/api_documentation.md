# Web Crawler - API Documentation

## Overview

The Advanced Web Crawler API is a RESTful web service that provides comprehensive web scraping, data extraction, and analytics capabilities. This documentation covers all available endpoints, request/response formats, authentication mechanisms, and usage examples.

## Base URL

```
http://localhost:8000
```

## Authentication

The API uses JSON Web Token (JWT) authentication. Include the token in the Authorization header for all protected endpoints:

```
Authorization: Bearer <your_jwt_token>
```

### Token Expiration
- **Default expiration**: 30 minutes
- **Refresh**: Re-authenticate to get a new token
- **Format**: JWT (JSON Web Token)

## Rate Limiting

The API implements rate limiting to ensure fair usage:

- **Limit**: 100 requests per hour per IP address
- **Headers included in response**:
  - `X-RateLimit-Limit`: Maximum requests allowed
  - `X-RateLimit-Remaining`: Remaining requests in current window
  - `X-RateLimit-Reset`: Time when the rate limit resets

## Response Format

All API responses follow a consistent JSON format:

### Success Response
```json
{
  "data": { ... },
  "message": "Success",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Error Response
```json
{
  "detail": "Error description",
  "error_code": "ERROR_CODE",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid request data |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Access denied |
| 404 | Not Found - Resource not found |
| 422 | Validation Error - Invalid input data |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Server error |

---

# Authentication Endpoints

## Register User

Create a new user account.

**Endpoint:** `POST /auth/signup`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "secure_password",
  "full_name": "John Doe"
}
```

**Validation Rules:**
- `email`: Valid email format, unique
- `password`: Minimum 8 characters
- `full_name`: Optional, maximum 100 characters

**Response (201):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "is_verified": false,
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses:**
```json
// Email already exists (400)
{
  "detail": "Email already registered"
}

// Validation error (422)
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## Login

Authenticate user and receive access token.

**Endpoint:** `POST /auth/login`

**Request Body (Form Data):**
```
username: user@example.com
password: secure_password
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Response (401):**
```json
{
  "detail": "Incorrect email or password"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=secure_password"
```

---

# User Management Endpoints

## Get User Profile

Retrieve current user's profile information.

**Endpoint:** `GET /users/profile`

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "is_verified": false,
  "created_at": "2024-01-15T10:30:00Z"
}
```

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/users/profile" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Update User Profile

Update user profile information.

**Endpoint:** `PUT /users/profile`

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "full_name": "John Smith",
  "password": "new_secure_password"
}
```

**Response (200):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Smith",
  "is_active": true,
  "is_verified": false,
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

# Crawl Jobs Endpoints

## Create Crawl Job

Create a new web crawling job.

**Endpoint:** `POST /crawl-jobs/`

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "News Website Crawler",
  "description": "Extract news articles from major publications",
  "target_urls": [
    "https://example-news.com/latest",
    "https://tech-news.com/headlines"
  ],
  "extraction_rules": {
    "title": "h1, .headline",
    "content": ".article-content, .story-body",
    "author": ".byline, .author-name",
    "publish_date": ".publish-date, time[datetime]",
    "tags": ".tags a, .categories a",
    "image_url": ".featured-image img@src"
  },
  "scheduled_at": "2024-01-15T14:00:00Z"
}
```

**Field Descriptions:**
- `name`: Job identifier (required, max 200 chars)
- `description`: Job description (optional, max 1000 chars)
- `target_urls`: List of URLs to crawl (required, max 100 URLs)
- `extraction_rules`: CSS selector mapping (required)
- `scheduled_at`: When to run the job (optional, defaults to immediate)

**CSS Selector Format:**
- Text extraction: `"title": "h1"`
- Attribute extraction: `"image_url": "img@src"`
- Multiple elements: `"links": "a[href]"`

**Response (200):**
```json
{
  "id": 1,
  "user_id": 1,
  "name": "News Website Crawler",
  "description": "Extract news articles from major publications",
  "target_urls": [
    "https://example-news.com/latest"
  ],
  "extraction_rules": {
    "title": "h1, .headline",
    "content": ".article-content"
  },
  "status": "pending",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "started_at": null,
  "completed_at": null,
  "scheduled_at": "2024-01-15T14:00:00Z"
}
```

**Status Values:**
- `pending`: Job created, waiting to start
- `running`: Job currently executing
- `completed`: Job finished successfully
- `failed`: Job encountered errors

## List Crawl Jobs

Retrieve all crawl jobs for the authenticated user.

**Endpoint:** `GET /crawl-jobs/`

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum records to return (default: 100, max: 1000)

**Response (200):**
```json
[
  {
    "id": 1,
    "name": "News Crawler",
    "description": "Daily news extraction",
    "status": "completed",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:35:00Z",
    "started_at": "2024-01-15T10:30:30Z",
    "completed_at": "2024-01-15T10:35:00Z"
  },
  {
    "id": 2,
    "name": "Product Scraper",
    "description": "E-commerce product monitoring",
    "status": "running",
    "created_at": "2024-01-15T11:00:00Z",
    "updated_at": "2024-01-15T11:00:00Z",
    "started_at": "2024-01-15T11:00:30Z",
    "completed_at": null
  }
]
```

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/crawl-jobs/?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Get Crawl Job Details

Retrieve detailed information about a specific crawl job.

**Endpoint:** `GET /crawl-jobs/{job_id}`

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Path Parameters:**
- `job_id`: Integer ID of the crawl job

**Response (200):**
```json
{
  "id": 1,
  "user_id": 1,
  "name": "News Website Crawler",
  "description": "Extract news articles",
  "target_urls": [
    "https://example-news.com/latest"
  ],
  "extraction_rules": {
    "title": "h1",
    "content": ".article-content"
  },
  "status": "completed",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:35:00Z",
  "started_at": "2024-01-15T10:30:30Z",
  "completed_at": "2024-01-15T10:35:00Z",
  "scheduled_at": null
}
```

## Update Crawl Job

Update an existing crawl job (only pending jobs can be updated).

**Endpoint:** `PUT /crawl-jobs/{job_id}`

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:** (All fields optional)
```json
{
  "name": "Updated News Crawler",
  "description": "Updated description",
  "target_urls": [
    "https://new-news-site.com"
  ],
  "extraction_rules": {
    "title": "h1.new-title",
    "content": ".new-content"
  },
  "scheduled_at": "2024-01-16T14:00:00Z"
}
```

**Response (200):**
```json
{
  "id": 1,
  "name": "Updated News Crawler",
  "status": "pending",
  "updated_at": "2024-01-15T12:00:00Z"
}
```

**Error Response (400):**
```json
{
  "detail": "Cannot update job in 'running' status"
}
```

## Delete Crawl Job

Delete a crawl job and all associated data.

**Endpoint:** `DELETE /crawl-jobs/{job_id}`

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "message": "Crawl job deleted successfully"
}
```

**Error Response (404):**
```json
{
  "detail": "Crawl job not found"
}
```

## Get Job Status

Get the current status and progress of a crawl job.

**Endpoint:** `GET /crawl-jobs/{job_id}/status`

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "id": 1,
  "status": "running",
  "started_at": "2024-01-15T10:30:30Z",
  "completed_at": null,
  "progress": {
    "total_urls": 10,
    "completed_urls": 7,
    "failed_urls": 1,
    "percentage": 80.0
  },
  "current_url": "https://example.com/page8",
  "estimated_completion": "2024-01-15T10:35:00Z"
}
```

## Get Extracted Data

Retrieve data extracted from a completed crawl job.

**Endpoint:** `GET /crawl-jobs/{job_id}/data`

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum records to return (default: 100)
- `format` (optional): Response format - 'json' or 'csv' (default: 'json')

**Response (200):**
```json
[
  {
    "id": 1,
    "url": "https://example.com/article-1",
    "data": {
      "title": "Breaking News: Technology Advances",
      "content": "In a groundbreaking development...",
      "author": "John Reporter",
      "publish_date": "2024-01-15",
      "tags": ["technology", "innovation", "news"],
      "image_url": "https://example.com/images/tech.jpg"
    },
    "extracted_at": "2024-01-15T10:35:00Z"
  },
  {
    "id": 2,
    "url": "https://example.com/article-2",
    "data": {
      "title": "Market Analysis: Q1 Results",
      "content": "The first quarter results show...",
      "author": "Jane Analyst",
      "publish_date": "2024-01-14",
      "tags": ["finance", "market", "analysis"],
      "image_url": null
    },
    "extracted_at": "2024-01-15T10:35:15Z"
  }
]
```

**CSV Response (format=csv):**
```csv
id,url,title,content,author,publish_date,tags,image_url,extracted_at
1,https://example.com/article-1,"Breaking News: Technology Advances","In a groundbreaking development...","John Reporter","2024-01-15","technology,innovation,news","https://example.com/images/tech.jpg","2024-01-15T10:35:00Z"
```

**cURL Example:**
```bash
# JSON format
curl -X GET "http://localhost:8000/crawl-jobs/1/data?limit=50" \
  -H "Authorization: Bearer YOUR_TOKEN"

# CSV format
curl -X GET "http://localhost:8000/crawl-jobs/1/data?format=csv" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -o extracted_data.csv
```

---

# Reports Endpoints

## Create Report

Generate an analytics report from one or more crawl jobs.

**Endpoint:** `POST /reports/`

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Weekly News Analysis",
  "description": "Comprehensive analysis of news data collected this week",
  "crawl_job_ids": [1, 2, 3, 4, 5]
}
```

**Response (200):**
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Weekly News Analysis",
  "description": "Comprehensive analysis of news data collected this week",
  "crawl_job_ids": [1, 2, 3, 4, 5],
  "report_data": {
    "summary": {
      "total_jobs": 5,
      "total_urls_crawled": 250,
      "successful_extractions": 238,
      "failed_extractions": 12,
      "success_rate": 95.2,
      "average_processing_time": 2.3
    },
    "field_analysis": {
      "common_fields": ["title", "content", "author", "publish_date"],
      "field_distribution": {
        "title": 238,
        "content": 235,
        "author": 220,
        "publish_date": 225,
        "tags": 180,
        "image_url": 150
      },
      "field_success_rates": {
        "title": 100.0,
        "content": 98.7,
        "author": 92.4,
        "publish_date": 94.5,
        "tags": 75.6,
        "image_url": 63.0
      }
    },
    "url_analysis": {
      "domains": {
        "example-news.com": {
          "urls_crawled": 100,
          "success_rate": 98.0,
          "average_response_time": 1.2
        },
        "tech-news.com": {
          "urls_crawled": 75,
          "success_rate": 96.0,
          "average_response_time": 1.8
        }
      },
      "response_codes": {
        "200": 238,
        "404": 8,
        "403": 3,
        "500": 1
      }
    },
    "content_analysis": {
      "average_content_length": 1250,
      "most_common_words": [
        {"word": "technology", "count": 145},
        {"word": "innovation", "count": 89},
        {"word": "market", "count": 76}
      ],
      "language_distribution": {
        "en": 230,
        "es": 5,
        "fr": 3
      }
    },
    "temporal_analysis": {
      "crawl_duration": {
        "fastest_job": 45.2,
        "slowest_job": 180.5,
        "average_job": 95.8
      },
      "hourly_distribution": {
        "00": 5, "01": 3, "02": 8, 
        "14": 45, "15": 52, "16": 38
      }
    }
  },
  "created_at": "2024-01-15T12:00:00Z"
}
```

## List Reports

Retrieve all reports for the authenticated user.

**Endpoint:** `GET /reports/`

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum records to return (default: 100)

**Response (200):**
```json
[
  {
    "id": 1,
    "title": "Weekly News Analysis",
    "description": "Analysis of news data from this week",
    "crawl_job_ids": [1, 2, 3],
    "created_at": "2024-01-15T12:00:00Z"
  },
  {
    "id": 2,
    "title": "Product Price Monitoring",
    "description": "E-commerce price tracking report",
    "crawl_job_ids": [4, 5],
    "created_at": "2024-01-14T09:30:00Z"
  }
]
```

## Get Report Details

Retrieve detailed information about a specific report.

**Endpoint:** `GET /reports/{report_id}`

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Weekly News Analysis",
  "description": "Analysis of news data from this week",
  "crawl_job_ids": [1, 2, 3],
  "report_data": {
    // Full report data as shown in create response
  },
  "created_at": "2024-01-15T12:00:00Z"
}
```

---

# Error Handling

## Error Response Format

All errors follow a consistent JSON format:

```json
{
  "detail": "Human-readable error message",
  "error_code": "MACHINE_READABLE_CODE",
  "timestamp": "2024-01-15T10:30:00Z",
  "path": "/crawl-jobs/123",
  "method": "GET"
}
```

## Common Error Codes

| Code | Description | HTTP Status |
|------|-------------|-------------|
| `INVALID_CREDENTIALS` | Invalid username/password | 401 |
| `TOKEN_EXPIRED` | JWT token has expired | 401 |
| `INVALID_TOKEN` | JWT token is malformed | 401 |
| `RESOURCE_NOT_FOUND` | Requested resource doesn't exist | 404 |
| `PERMISSION_DENIED` | User lacks required permissions | 403 |
| `VALIDATION_ERROR` | Request data validation failed | 422 |
| `RATE_LIMIT_EXCEEDED` | Too many requests | 429 |
| `INTERNAL_ERROR` | Server-side error | 500 |
| `CRAWL_JOB_RUNNING` | Cannot modify running job | 400 |
| `INVALID_CSS_SELECTOR` | CSS selector syntax error | 422 |
| `URL_NOT_ACCESSIBLE` | Target URL unreachable | 400 |

## Validation Errors

Validation errors provide detailed field-level information:

```json
{
  "detail": [
    {
      "loc": ["body", "target_urls", 0],
      "msg": "invalid url format",
      "type": "value_error.url",
      "ctx": {"url": "not-a-valid-url"}
    },
    {
      "loc": ["body", "extraction_rules", "title"],
      "msg": "invalid CSS selector",
      "type": "value_error.css_selector"
    }
  ]
}
```

---

# Best Practices

## Authentication Security
- Store JWT tokens securely
- Implement token refresh logic
- Use HTTPS in production
- Never expose tokens in URLs or logs

## Rate Limiting Management
- Implement exponential backoff
- Monitor rate limit headers
- Cache responses when possible
- Use webhooks instead of polling

## Error Handling
- Always check HTTP status codes
- Parse error responses for details
- Implement retry logic for transient errors
- Log errors for debugging

## Performance Optimization
- Use pagination for large datasets
- Request only needed fields
- Implement request timeouts
- Use compression when available

## Data Extraction Tips
- Test CSS selectors in browser first
- Handle missing elements gracefully
- Use specific selectors over generic ones
- Consider page load times and dynamic content