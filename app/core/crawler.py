import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
import logging
from fake_useragent import UserAgent
import random
from .robots_checker import RobotsChecker
from .data_extractor import DataExtractor

logger = logging.getLogger(__name__)

class SimpleCrawler:
    def __init__(self, 
                 max_concurrent: int = 5, 
                 delay_range: tuple = (1, 2),
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
            allowed_urls = []
            for url in urls:
                if self.robots_checker.can_crawl(url):
                    allowed_urls.append(url)
                else:
                    logger.warning(f"URL blocked by robots.txt: {url}")
        else:
            allowed_urls = urls
        
        if not allowed_urls:
            logger.warning("No URLs to crawl after robots.txt filtering")
            return []
        
        semaphore = asyncio.Semaphore(self.max_concurrent)
        tasks = [
            self._crawl_single_url(semaphore, url, extraction_rules) 
            for url in allowed_urls
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        valid_results = []
        
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Crawl task failed: {result}")
            else:
                valid_results.append(result)
        
        return valid_results
    
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
                
                logger.info(f"Crawling URL: {url}")
                
                async with self.session.get(url, headers=headers) as response:
                    if response.status == 200:
                        html = await response.text()
                        result = self.data_extractor.extract_data(html, url, extraction_rules)
                        logger.info(f"Successfully crawled: {url}")
                        return result
                    else:
                        error_msg = f"HTTP {response.status}"
                        logger.warning(f"Failed to crawl {url}: {error_msg}")
                        return {
                            "url": url, 
                            "error": error_msg,
                            "data": {}
                        }
                        
            except Exception as e:
                error_msg = str(e)
                logger.error(f"Error crawling {url}: {error_msg}")
                return {"url": url, "error": error_msg, "data": {}}
            finally:
                delay = random.uniform(*self.delay_range)
                await asyncio.sleep(delay)