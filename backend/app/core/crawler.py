import asyncio
import aiohttp
from typing import List, Dict, Optional
import logging
from fake_useragent import UserAgent
import random
from .robots_checker import RobotsChecker
from .data_extractor import DataExtractor

logger = logging.getLogger(__name__)

class AdvancedWebCrawler:
    def __init__(self, 
                 max_concurrent: int = 10, 
                 delay_range: tuple = (1, 3),
                 user_agent: Optional[str] = None,
                 respect_robots: bool = True):
        self.max_concurrent = max_concurrent
        self.delay_range = delay_range
        self.session = None
        self.ua = UserAgent()
        self.user_agent = user_agent or self.ua.random
        self.respect_robots = respect_robots
        self.robots_checker = RobotsChecker(self.user_agent) if respect_robots else None
        self.data_extractor = DataExtractor()
        
    async def __aenter__(self):
        timeout = aiohttp.ClientTimeout(total=30)
        self.session = aiohttp.ClientSession(timeout=timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def crawl_urls(self, urls: List[str], extraction_rules: Dict[str, str]) -> List[Dict]:
        """Crawl multiple URLs with extraction rules"""
        if self.respect_robots:
            allowed_urls = [url for url in urls if self.robots_checker.can_crawl(url)]
            blocked_urls = set(urls) - set(allowed_urls)
            
            if blocked_urls:
                logger.info(f"Blocked {len(blocked_urls)} URLs due to robots.txt")
        else:
            allowed_urls = urls
        
        semaphore = asyncio.Semaphore(self.max_concurrent)
        tasks = [
            self._crawl_single_url(semaphore, url, extraction_rules) 
            for url in allowed_urls
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [r for r in results if not isinstance(r, Exception)]
    
    async def _crawl_single_url(self, semaphore, url: str, extraction_rules: Dict) -> Dict:
        """Crawl a single URL and extract data"""
        async with semaphore:
            try:
                headers = {
                    'User-Agent': self.user_agent,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                }
                
                async with self.session.get(url, headers=headers) as response:
                    if response.status == 200:
                        html = await response.text()
                        return self.data_extractor.extract_data(html, url, extraction_rules)
                    else:
                        return {
                            "url": url, 
                            "error": f"HTTP {response.status}",
                            "data": {}
                        }
                        
            except Exception as e:
                logger.error(f"Error crawling {url}: {e}")
                return {"url": url, "error": str(e), "data": {}}
            finally:
                delay = random.uniform(*self.delay_range)
                await asyncio.sleep(delay)