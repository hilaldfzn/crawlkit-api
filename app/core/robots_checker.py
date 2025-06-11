import requests
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin, urlparse
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class RobotsChecker:
    def __init__(self, user_agent: str = "*"):
        self.user_agent = user_agent
        self.robots_cache: Dict[str, RobotFileParser] = {}
    
    def can_crawl(self, url: str) -> bool:
        """Check if URL can be crawled according to robots.txt"""
        try:
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            
            if base_url not in self.robots_cache:
                self._load_robots_txt(base_url)
            
            robots_parser = self.robots_cache.get(base_url)
            if robots_parser:
                return robots_parser.can_fetch(self.user_agent, url)
            
            return True
            
        except Exception as e:
            logger.warning(f"Error checking robots.txt for {url}: {e}")
            return True
    
    def _load_robots_txt(self, base_url: str):
        """Load and parse robots.txt for a domain"""
        try:
            robots_url = urljoin(base_url, "/robots.txt")
            response = requests.get(robots_url, timeout=10)
            
            if response.status_code == 200:
                robots_parser = RobotFileParser()
                robots_parser.set_url(robots_url)
                robots_parser.read()
                self.robots_cache[base_url] = robots_parser
            else:
                self.robots_cache[base_url] = None
                
        except Exception as e:
            logger.warning(f"Failed to load robots.txt from {base_url}: {e}")
            self.robots_cache[base_url] = None