import pytest
from backend.app.core.crawler import AdvancedWebCrawler

@pytest.mark.asyncio
async def test_crawler_basic_functionality():
    """Test basic crawler functionality"""
    crawler = AdvancedWebCrawler(respect_robots=False)
    
    urls = ["https://httpbin.org/html"]
    extraction_rules = {
        "title": "title",
        "headings": "h1"
    }
    
    async with crawler:
        results = await crawler.crawl_urls(urls, extraction_rules)
    
    assert len(results) == 1
    assert "data" in results[0]
    assert "url" in results[0]

@pytest.mark.asyncio
async def test_crawler_with_invalid_url():
    """Test crawler handling of invalid URLs"""
    crawler = AdvancedWebCrawler(respect_robots=False)
    
    urls = ["https://invalid-url-that-does-not-exist.com"]
    extraction_rules = {"title": "title"}
    
    async with crawler:
        results = await crawler.crawl_urls(urls, extraction_rules)
    
    assert len(results) == 1
    assert "error" in results[0]