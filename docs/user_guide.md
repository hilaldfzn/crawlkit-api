# Web Crawler - User Guide

## Table of Contents

1. [Getting Started](#getting-started)
2. [Understanding Web Crawling](#understanding-web-crawling)
3. [Setting Up Your Environment](#setting-up-your-environment)
4. [Your First Crawl Job](#your-first-crawl-job)
5. [Data Extraction Techniques](#data-extraction-techniques)
6. [Managing Crawl Jobs](#managing-crawl-jobs)
7. [Analytics and Reporting](#analytics-and-reporting)
8. [Best Practices](#best-practices)
9. [Common Use Cases](#common-use-cases)
10. [Troubleshooting](#troubleshooting)
11. [Advanced Features](#advanced-features)

---

## Getting Started

### What is the Web Crawler API?

The Web Crawler API is a powerful tool that allows you to automatically extract data from websites. Whether you're monitoring competitor prices, collecting news articles, or gathering research data, our API provides a robust and scalable solution for your web scraping needs.

### Key Benefits

- **No Coding Required**: Use our simple REST API to create crawl jobs
- **Respect for Robots.txt**: Ethical crawling that respects website policies
- **Scalable Processing**: Handle thousands of URLs efficiently
- **Rich Analytics**: Get insights into your crawling performance
- **Flexible Extraction**: Use CSS selectors to extract exactly what you need

### Prerequisites

Before you begin, you'll need:
- A registered account with the Web Crawler API
- Basic understanding of web technologies (HTML, CSS)
- An HTTP client (curl, Postman, or programming language of choice)

---

## Understanding Web Crawling

### How Web Crawling Works

Web crawling is the process of automatically visiting web pages and extracting specific information. Here's how our API works:

1. **Job Creation**: You define what websites to visit and what data to extract
2. **Queue Processing**: Your job is added to our processing queue
3. **Web Requests**: Our crawlers visit each URL you specified
4. **Data Extraction**: We use your CSS selectors to extract relevant data
5. **Storage**: Extracted data is stored and made available via the API

### Ethical Crawling

Our API follows best practices for ethical web crawling:

- **Robots.txt Compliance**: We automatically check and respect robots.txt files
- **Rate Limiting**: Requests are spaced out to avoid overwhelming target servers
- **User-Agent Identification**: We identify ourselves properly to web servers
- **Respectful Delays**: Built-in delays between requests

### Legal Considerations

When using our API, please ensure:
- You have permission to crawl the target websites
- You comply with the website's terms of service
- You respect copyright and intellectual property rights
- You follow applicable data protection regulations (GDPR, CCPA, etc.)

---

## Setting Up Your Environment

### Account Registration

1. **Sign Up**: Create your account at `/auth/signup`
2. **Email Verification**: Verify your email address (if required)
3. **API Access**: Obtain your authentication credentials

### Authentication Setup

#### Step 1: Register Your Account

```bash
curl -X POST "http://localhost:8000/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your-email@example.com",
    "password": "secure_password_123",
    "full_name": "Your Name"
  }'
```

#### Step 2: Login and Get Token

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=your-email@example.com&password=secure_password_123"
```

Save the returned token - you'll need it for all subsequent requests:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Step 3: Test Your Setup

```bash
curl -X GET "http://localhost:8000/users/profile" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Environment Variables

For convenience, set your token as an environment variable:

```bash
# Linux/macOS
export WEBCRAWLER_TOKEN="your_token_here"

# Windows
set WEBCRAWLER_TOKEN=your_token_here

# Use in commands
curl -H "Authorization: Bearer $WEBCRAWLER_TOKEN" ...
```

---

## Your First Crawl Job

### Example: Extracting News Headlines

Let's create a simple crawl job to extract news headlines from a website.

#### Step 1: Analyze the Target Website

Before creating a crawl job, visit the target website and inspect its HTML structure:

1. **Open Developer Tools**: Right-click on the page and select "Inspect Element"
2. **Identify Target Elements**: Find the HTML elements containing the data you want
3. **Note CSS Selectors**: Write down the CSS selectors for each piece of data

Example HTML structure:
```html
<article class="news-item">
  <h2 class="headline">Breaking: Tech Company Announces New Product</h2>
  <p class="summary">The company revealed details about their latest innovation...</p>
  <span class="author">By John Smith</span>
  <time class="publish-date">2024-01-15</time>
</article>
```

#### Step 2: Create Your First Crawl Job

```bash
curl -X POST "http://localhost:8000/crawl-jobs/" \
  -H "Authorization: Bearer $WEBCRAWLER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My First News Crawler",
    "description": "Extract headlines and summaries from news website",
    "target_urls": [
      "https://example-news.com/latest"
    ],
    "extraction_rules": {
      "headline": ".headline",
      "summary": ".summary", 
      "author": ".author",
      "publish_date": ".publish-date"
    }
  }'
```

#### Step 3: Monitor Job Progress

The API will return a job ID. Use it to check the status:

```bash
# Check job status
curl -X GET "http://localhost:8000/crawl-jobs/1/status" \
  -H "Authorization: Bearer $WEBCRAWLER_TOKEN"

# Response
{
  "id": 1,
  "status": "completed",
  "started_at": "2024-01-15T10:30:00Z",
  "completed_at": "2024-01-15T10:32:15Z"
}
```

#### Step 4: Retrieve Extracted Data

```bash
curl -X GET "http://localhost:8000/crawl-jobs/1/data" \
  -H "Authorization: Bearer $WEBCRAWLER_TOKEN"
```

Example response:
```json
[
  {
    "id": 1,
    "url": "https://example-news.com/latest",
    "data": {
      "headline": "Breaking: Tech Company Announces New Product",
      "summary": "The company revealed details about their latest innovation...",
      "author": "By John Smith",
      "publish_date": "2024-01-15"
    },
    "extracted_at": "2024-01-15T10:31:45Z"
  }
]
```

---

## Data Extraction Techniques

### CSS Selectors Guide

CSS selectors are the key to extracting the right data. Here's a comprehensive guide:

#### Basic Selectors

| Selector | Description | Example |
|----------|-------------|---------|
| `h1` | Element selector | Select all `<h1>` elements |
| `.class` | Class selector | Select elements with class="class" |
| `#id` | ID selector | Select element with id="id" |
| `*` | Universal selector | Select all elements |

#### Combination Selectors

| Selector | Description | Example |
|----------|-------------|---------|
| `div p` | Descendant | Paragraphs inside div elements |
| `div > p` | Direct child | Paragraphs directly inside div |
| `h1 + p` | Adjacent sibling | Paragraph immediately after h1 |
| `h1 ~ p` | General sibling | Paragraphs that follow h1 |

#### Attribute Selectors

| Selector | Description | Example |
|----------|-------------|---------|
| `a[href]` | Has attribute | Links with href attribute |
| `a[href="url"]` | Exact match | Links with specific href |
| `a[href^="https"]` | Starts with | Links starting with https |
| `a[href$=".pdf"]` | Ends with | Links ending with .pdf |
| `a[href*="download"]` | Contains | Links containing "download" |

#### Pseudo-selectors

| Selector | Description | Example |
|----------|-------------|---------|
| `:first-child` | First child element | First paragraph in a div |
| `:last-child` | Last child element | Last item in a list |
| `:nth-child(n)` | Nth child element | 3rd paragraph |
| `:not(selector)` | Not matching | All except hidden elements |

### Attribute Extraction

To extract attributes instead of text content, use the `@` syntax:

```json
{
  "image_url": "img@src",
  "link_url": "a@href",
  "alt_text": "img@alt",
  "custom_data": "[data-value]@data-value"
}
```

### Advanced Extraction Examples

#### E-commerce Product Data
```json
{
  "product_name": ".product-title h1",
  "price": ".price-current",
  "original_price": ".price-original",
  "rating": ".rating-stars@data-rating",
  "reviews_count": ".reviews-count",
  "availability": ".stock-status",
  "images": ".product-gallery img@src",
  "description": ".product-description p",
  "features": ".features-list li"
}
```

#### Social Media Posts
```json
{
  "post_text": ".post-content",
  "author": ".author-name",
  "timestamp": ".post-time@datetime",
  "likes": ".like-count",
  "shares": ".share-count",
  "comments": ".comment-count",
  "hashtags": ".hashtag",
  "mentions": ".mention"
}
```

#### Job Listings
```json
{
  "job_title": ".job-title",
  "company": ".company-name",
  "location": ".job-location",
  "salary_range": ".salary",
  "job_type": ".employment-type",
  "experience_level": ".experience-required",
  "skills": ".required-skills .skill",
  "application_url": ".apply-button@href",
  "posted_date": ".post-date"
}
```

### Handling Dynamic Content

Some websites load content dynamically with JavaScript. While our crawler primarily handles static HTML, here are strategies for dynamic content:

#### Strategy 1: Find Alternative Endpoints
Many sites have API endpoints or static pages with the same data:
- Check for `/api/` endpoints
- Look for RSS/XML feeds
- Try mobile versions (often simpler HTML)

#### Strategy 2: Use Specific Timing
If content loads after the initial page load:
- Target the final state selectors
- Use unique identifiers that appear after loading

#### Strategy 3: Alternative Selectors
Find elements that exist in the initial HTML:
- Data attributes that get populated
- Script tags containing JSON data
- Hidden elements with the information

---

## Managing Crawl Jobs

### Job Lifecycle

Understanding the job lifecycle helps you manage your crawling effectively:

1. **Created** → Job is created but not yet started
2. **Pending** → Job is queued for processing
3. **Running** → Job is actively crawling
4. **Completed** → Job finished successfully
5. **Failed** → Job encountered errors

### Viewing Your Jobs

#### List All Jobs
```bash
curl -X GET "http://localhost:8000/crawl-jobs/" \
  -H "Authorization: Bearer $WEBCRAWLER_TOKEN"
```

#### Filter and Paginate
```bash
# Get jobs 11-20
curl -X GET "http://localhost:8000/crawl-jobs/?skip=10&limit=10" \
  -H "Authorization: Bearer $WEBCRAWLER_TOKEN"
```

### Updating Jobs

You can update jobs that haven't started yet:

```bash
curl -X PUT "http://localhost:8000/crawl-jobs/123" \
  -H "Authorization: Bearer $WEBCRAWLER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Job Name",
    "target_urls": ["https://new-site.com"],
    "extraction_rules": {
      "title": "h1.new-selector"
    }
  }'
```

### Deleting Jobs

Remove jobs you no longer need:

```bash
curl -X DELETE "http://localhost:8000/crawl-jobs/123" \
  -H "Authorization: Bearer $WEBCRAWLER_TOKEN"
```

**Note**: This deletes the job and all associated extracted data.

### Scheduling Jobs

Schedule jobs to run at specific times:

```json
{
  "name": "Daily News Scraper",
  "target_urls": ["https://news.example.com"],
  "extraction_rules": {"headline": "h1"},
  "scheduled_at": "2024-01-16T09:00:00Z"
}
```

---

## Analytics and Reporting

### Understanding Job Analytics

Each completed job provides valuable analytics:

#### Success Metrics
- **Total URLs**: Number of URLs attempted
- **Successful Extractions**: URLs that returned data
- **Failed Extractions**: URLs that failed or returned no data
- **Success Rate**: Percentage of successful extractions

#### Performance Metrics
- **Processing Time**: How long the job took
- **Average Response Time**: Time per URL
- **Data Quality Score**: Percentage of fields successfully extracted

### Creating Reports

Reports aggregate data across multiple crawl jobs:

```bash
curl -X POST "http://localhost:8000/reports/" \
  -H "Authorization: Bearer $WEBCRAWLER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Weekly Analysis",
    "description": "Analysis of this week'\''s crawling activity",
    "crawl_job_ids": [1, 2, 3, 4, 5]
  }'
```

### Report Insights

Reports provide comprehensive insights:

#### Summary Statistics
- Total jobs analyzed
- Overall success rate
- Data volume extracted
- Processing efficiency

#### Field Analysis
- Most commonly extracted fields
- Field success rates
- Data completeness scores

#### Domain Analysis
- Performance by website
- Response time variations
- Success rates by domain

#### Temporal Analysis
- Peak performance times
- Processing duration trends
- Optimal crawling windows

### Viewing Reports

```bash
# List all reports
curl -X GET "http://localhost:8000/reports/" \
  -H "Authorization: Bearer $WEBCRAWLER_TOKEN"

# Get specific report
curl -X GET "http://localhost:8000/reports/1" \
  -H "Authorization: Bearer $WEBCRAWLER_TOKEN"
```

---

## Best Practices

### Planning Your Crawl Jobs

#### 1. Start Small
- Begin with a few URLs to test your selectors
- Verify data quality before scaling up
- Iterate and improve your extraction rules

#### 2. Analyze Target Sites
- Study the HTML structure thoroughly
- Check for consistent patterns across pages
- Identify unique identifiers for reliable extraction

#### 3. Test Selectors
Use browser developer tools to test your CSS selectors:

```javascript
// In browser console
document.querySelectorAll('.your-selector')
```

### Optimizing Performance

#### 1. Efficient URL Selection
- Target specific pages with the data you need
- Avoid unnecessary pages (about, contact, etc.)
- Use sitemap.xml to find relevant URLs

#### 2. Smart Scheduling
- Schedule jobs during off-peak hours
- Distribute large jobs across time
- Avoid overlapping similar jobs

#### 3. Resource Management
- Monitor your API usage limits
- Use appropriate delays between requests
- Consider the target site's server capacity

### Data Quality Assurance

#### 1. Validation Rules
Implement checks for your extracted data:

```python
def validate_extracted_data(data):
    checks = []
    
    # Check if title exists and has reasonable length
    if 'title' in data and len(data['title']) > 10:
        checks.append('title_valid')
    
    # Check if price is numeric
    if 'price' in data:
        try:
            float(data['price'].replace(', '').replace(',', ''))
            checks.append('price_valid')
        except ValueError:
            pass
    
    return checks
```

#### 2. Monitoring and Alerts
Set up monitoring for:
- Sudden drops in success rates
- Changes in data structure
- Unusual processing times
- Error pattern changes

#### 3. Regular Review
- Review extraction rules monthly
- Update selectors when sites change
- Archive old, unused jobs

### Respecting Target Websites

#### 1. Follow robots.txt
Our API automatically checks robots.txt, but you should understand what it means:

```
User-agent: *
Disallow: /private/
Crawl-delay: 1
```

This means:
- Don't crawl `/private/` directory
- Wait 1 second between requests

#### 2. Reasonable Request Rates
- Don't overwhelm small websites
- Consider the site's capacity
- Use longer delays for slower sites

#### 3. Identify Yourself
Our API identifies itself properly, but if contacted by site owners:
- Be transparent about your use case
- Respect requests to stop crawling
- Offer to share insights if beneficial

---

## Common Use Cases

### 1. E-commerce Price Monitoring

**Scenario**: Monitor competitor prices for your products

**Setup**:
```json
{
  "name": "Competitor Price Monitor",
  "target_urls": [
    "https://competitor1.com/product/123",
    "https://competitor2.com/item/456"
  ],
  "extraction_rules": {
    "product_name": ".product-title",
    "current_price": ".price-current",
    "original_price": ".price-original",
    "stock_status": ".availability",
    "rating": ".rating@data-rating",
    "seller": ".sold-by"
  }
}
```

**Best Practices**:
- Run daily to track price changes
- Monitor stock availability
- Set up alerts for significant price drops
- Respect crawl delays for e-commerce sites

### 2. News and Content Aggregation

**Scenario**: Collect articles from multiple news sources

**Setup**:
```json
{
  "name": "Tech News Aggregator",
  "target_urls": [
    "https://techcrunch.com/",
    "https://arstechnica.com/",
    "https://wired.com/category/business/"
  ],
  "extraction_rules": {
    "headline": "h1, .post-title, .headline",
    "summary": ".excerpt, .summary, .lead",
    "author": ".author, .byline",
    "publish_date": ".date, .timestamp, time",
    "category": ".category, .tag",
    "read_time": ".read-time",
    "article_url": ".read-more@href"
  }
}
```

**Advanced Features**:
- Deduplicate articles by title similarity
- Categorize content automatically
- Track trending topics
- Generate daily digest reports

### 3. Job Market Analysis

**Scenario**: Track job postings in your industry

**Setup**:
```json
{
  "name": "Data Science Job Tracker",
  "target_urls": [
    "https://jobs.example.com/search?q=data+scientist",
    "https://careers.example.com/data-science-jobs"
  ],
  "extraction_rules": {
    "job_title": ".job-title",
    "company": ".company-name",
    "location": ".location",
    "salary_range": ".salary",
    "experience": ".experience-level",
    "skills": ".required-skills .skill",
    "remote_option": ".remote-friendly",
    "post_date": ".posted-date",
    "apply_url": ".apply-link@href"
  }
}
```

**Analysis Ideas**:
- Salary trend analysis
- Most in-demand skills
- Geographic distribution
- Remote work availability

### 4. Real Estate Market Monitoring

**Scenario**: Track property listings and prices

**Setup**:
```json
{
  "name": "Real Estate Monitor",
  "target_urls": [
    "https://realestate.example.com/city/neighborhood"
  ],
  "extraction_rules": {
    "property_title": ".listing-title",
    "price": ".price",
    "bedrooms": ".beds",
    "bathrooms": ".baths",
    "square_feet": ".sqft",
    "property_type": ".property-type",
    "listing_date": ".listed-date",
    "address": ".address",
    "description": ".description",
    "images": ".photo-gallery img@src",
    "agent": ".listing-agent",
    "listing_url": ".listing-link@href"
  }
}
```

**Market Insights**:
- Average price per square foot
- Inventory trends
- Days on market analysis
- Neighborhood comparisons

### 5. Academic Research Data Collection

**Scenario**: Collect research papers and citations

**Setup**:
```json
{
  "name": "Academic Paper Crawler",
  "target_urls": [
    "https://arxiv.org/list/cs.AI/recent",
    "https://scholar.google.com/scholar?q=machine+learning"
  ],
  "extraction_rules": {
    "paper_title": ".title",
    "authors": ".authors",
    "abstract": ".abstract",
    "publication_date": ".date",
    "journal": ".journal",
    "citations": ".citation-count",
    "keywords": ".keywords",
    "pdf_url": ".pdf-link@href",
    "doi": ".doi"
  }
}
```

**Research Applications**:
- Literature review automation
- Citation network analysis
- Trending research topics
- Author collaboration patterns

### 6. Social Media Monitoring

**Scenario**: Monitor brand mentions and sentiment

**Setup**:
```json
{
  "name": "Brand Mention Monitor",
  "target_urls": [
    "https://socialmedia.example.com/search?q=your-brand"
  ],
  "extraction_rules": {
    "post_text": ".post-content",
    "author": ".username",
    "post_date": ".timestamp",
    "likes": ".like-count",
    "shares": ".share-count",
    "comments": ".comment-count",
    "hashtags": ".hashtag",
    "post_url": ".post-link@href"
  }
}
```

**Monitoring Strategy**:
- Track mention volume
- Analyze sentiment trends
- Identify influential users
- Monitor competitor mentions

---

## Troubleshooting

### Common Issues and Solutions

#### 1. No Data Extracted

**Symptoms**: Job completes but returns empty data

**Possible Causes**:
- Incorrect CSS selectors
- Content loaded via JavaScript
- Site structure changed
- Access blocked

**Solutions**:
```bash
# Test your selectors manually
curl -s "https://target-site.com" | grep -i "your-target-content"

# Check if robots.txt blocks crawling
curl "https://target-site.com/robots.txt"

# Verify site accessibility
curl -I "https://target-site.com"
```

**Debugging Steps**:
1. Visit the target URL in your browser
2. Right-click and inspect the element you want to extract
3. Test the CSS selector in browser console:
   ```javascript
   document.querySelectorAll('your-selector')
   ```
4. Update your extraction rules with the correct selector

#### 2. Partial Data Extraction

**Symptoms**: Some fields extracted, others missing

**Analysis**:
```json
{
  "title": "Article Title",
  "content": "Article content...",
  "author": null,
  "date": null
}
```

**Solutions**:
- Check if missing elements exist on the page
- Try alternative selectors for missing fields
- Use more general selectors that work across page variations

**Alternative Selector Strategy**:
```json
{
  "author": ".author, .byline, .writer-name, [data-author]",
  "date": ".date, .timestamp, .published, time[datetime]"
}
```

#### 3. Rate Limiting Issues

**Symptoms**: HTTP 429 errors or slow processing

**Solutions**:
- Reduce the number of concurrent URLs
- Increase delays between requests
- Spread crawling across time periods
- Contact support for rate limit increases

#### 4. Authentication Errors

**Symptoms**: HTTP 401 or 403 errors

**Common Causes**:
- Expired JWT token
- Invalid token format
- Missing Authorization header

**Solutions**:
```bash
# Check token expiration
python3 -c "
import jwt
import json
token = 'your-token-here'
decoded = jwt.decode(token, options={'verify_signature': False})
print(json.dumps(decoded, indent=2))
"

# Get a new token
curl -X POST "http://localhost:8000/auth/login" \
  -d "username=your@email.com&password=yourpassword"
```

#### 5. Slow Job Processing

**Symptoms**: Jobs take much longer than expected

**Optimization Strategies**:
- Reduce the number of target URLs
- Simplify extraction rules
- Schedule during off-peak hours
- Check target site response times

**Performance Monitoring**:
```bash
# Check job progress
curl -X GET "http://localhost:8000/crawl-jobs/123/status" \
  -H "Authorization: Bearer $WEBCRAWLER_TOKEN"

# Monitor system performance
curl -X GET "http://localhost:8000/health" \
  -H "Authorization: Bearer $WEBCRAWLER_TOKEN"
```

### Getting Help

#### 1. Check Job Logs
Use the job status endpoint to get detailed error information:

```bash
curl -X GET "http://localhost:8000/crawl-jobs/123/status" \
  -H "Authorization: Bearer $WEBCRAWLER_TOKEN"
```

#### 2. Validate Your Extraction Rules
Before creating large jobs, test with a single URL:

```json
{
  "name": "Test Job",
  "target_urls": ["https://single-test-url.com"],
  "extraction_rules": {
    "test_field": "your-selector"
  }
}
```

#### 3. Use Browser Developer Tools
The browser's developer tools are your best friend:

1. **Elements Tab**: Inspect HTML structure
2. **Console Tab**: Test CSS selectors
3. **Network Tab**: Monitor HTTP requests
4. **Sources Tab**: View page source

#### 4. Community Resources
- **Documentation**: Always check the latest API docs
- **GitHub Issues**: Search for similar problems
- **Stack Overflow**: Use tags related to web scraping
- **Support Forums**: Engage with the community

#### 5. Contact Support
When contacting support, include:
- Job ID of the failing crawl
- Target URLs you're trying to crawl
- Expected vs. actual results
- Error messages or status codes
- Screenshots of the target website structure

---

## Advanced Features

### Webhook Notifications

Set up webhooks to receive real-time notifications about job completion:

```bash
curl -X POST "http://localhost:8000/webhooks/" \
  -H "Authorization: Bearer $WEBCRAWLER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-domain.com/webhook",
    "events": ["job.completed", "job.failed"],
    "secret": "your-webhook-secret"
  }'
```

**Webhook Payload Example**:
```json
{
  "event": "job.completed",
  "job_id": 123,
  "user_id": 1,
  "timestamp": "2024-01-15T10:35:00Z",
  "data": {
    "status": "completed",
    "total_urls": 50,
    "extracted_records": 48,
    "processing_time": 120.5,
    "success_rate": 96.0
  }
}
```

### Bulk Job Creation

Create multiple similar jobs efficiently:

```bash
curl -X POST "http://localhost:8000/crawl-jobs/bulk" \
  -H "Authorization: Bearer $WEBCRAWLER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "jobs": [
      {
        "name": "News Site 1",
        "target_urls": ["https://news1.com"],
        "extraction_rules": {"title": "h1", "content": ".content"}
      },
      {
        "name": "News Site 2",
        "target_urls": ["https://news2.com"],
        "extraction_rules": {"title": "h1", "content": ".article"}
      }
    ]
  }'
```

### Data Export Options

Export your data in various formats:

```bash
# Export as CSV
curl -X GET "http://localhost:8000/crawl-jobs/123/export?format=csv" \
  -H "Authorization: Bearer $WEBCRAWLER_TOKEN" \
  -o data.csv

# Export as Excel
curl -X GET "http://localhost:8000/crawl-jobs/123/export?format=excel&fields=title,author,date" \
  -H "Authorization: Bearer $WEBCRAWLER_TOKEN" \
  -o data.xlsx

# Export with filters
curl -X GET "http://localhost:8000/crawl-jobs/123/export?format=json&filter={\"author\":\"John\"}" \
  -H "Authorization: Bearer $WEBCRAWLER_TOKEN" \
  -o filtered_data.json
```

### Scheduled Recurring Jobs

Set up jobs that run automatically on a schedule:

```json
{
  "name": "Daily Price Monitor",
  "target_urls": ["https://shop.example.com/products"],
  "extraction_rules": {"price": ".price", "stock": ".availability"},
  "schedule": {
    "type": "recurring",
    "frequency": "daily",
    "time": "09:00:00",
    "timezone": "UTC"
  }
}
```

### Advanced Analytics

Access detailed analytics for your crawling operations:

```bash
# Get performance metrics
curl -X GET "http://localhost:8000/analytics/performance?days=30" \
  -H "Authorization: Bearer $WEBCRAWLER_TOKEN"

# Get success rate trends
curl -X GET "http://localhost:8000/analytics/success-rates?job_ids=1,2,3" \
  -H "Authorization: Bearer $WEBCRAWLER_TOKEN"

# Get domain-specific analytics
curl -X GET "http://localhost:8000/analytics/domains" \
  -H "Authorization: Bearer $WEBCRAWLER_TOKEN"
```

---

## Conclusion

The Advanced Web Crawler API provides a powerful and flexible solution for automated data extraction. By following the best practices and techniques outlined in this guide, you can:

- Extract data efficiently and ethically
- Build robust crawling workflows
- Monitor and optimize your operations
- Generate valuable insights from web data

### Next Steps

1. **Start Small**: Begin with simple crawl jobs to familiarize yourself with the API
2. **Iterate and Improve**: Refine your extraction rules based on results
3. **Scale Gradually**: Increase complexity and volume as you gain experience
4. **Monitor Performance**: Use analytics to optimize your crawling strategy
5. **Stay Updated**: Keep up with API updates and new features

### Additional Resources

- **API Documentation**: Complete reference for all endpoints
- **Community Forum**: Connect with other users and share experiences
- **Blog**: Tips, tutorials, and use case studies
- **Support**: Technical support for troubleshooting and optimization

Happy crawling! 🕷️