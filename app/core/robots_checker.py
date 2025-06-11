import requests
import certifi
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin, urlparse
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class RobotsChecker:
    def __init__(self, user_agent: str = "*", verify_ssl: bool = True):
        self.user_agent = user_agent
        self.verify_ssl = verify_ssl
        self.robots_cache: Dict[str, RobotFileParser] = {}
        
        # Configure requests session with SSL
        self.session = requests.Session()
        if verify_ssl:
            self.session.verify = certifi.where()
        else:
            self.session.verify = False
            # Disable SSL warnings when verification is disabled
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    def can_crawl(self, url: str) -> bool:
        """Check if URL can be crawled according to robots.txt"""
        try:
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            
            if base_url not in self.robots_cache:
                self._load_robots_txt(base_url)
            
            robots_parser = self.robots_cache.get(base_url)
            if robots_parser:
                can_fetch = robots_parser.can_fetch(self.user_agent, url)
                logger.info(f"Robots.txt check for {url}: {'ALLOWED' if can_fetch else 'BLOCKED'}")
                return can_fetch
            
            # If no robots.txt found, allow crawling
            logger.info(f"No robots.txt found for {base_url}, allowing crawl")
            return True
            
        except Exception as e:
            logger.warning(f"Error checking robots.txt for {url}: {e}")
            return True
    
    def _load_robots_txt(self, base_url: str):
        """Load and parse robots.txt for a domain"""
        try:
            robots_url = urljoin(base_url, "/robots.txt")
            logger.info(f"Loading robots.txt from: {robots_url}")
            
            response = self.session.get(
                robots_url, 
                timeout=10,
                headers={'User-Agent': self.user_agent}
            )
            
            if response.status_code == 200:
                robots_parser = RobotFileParser()
                robots_parser.set_url(robots_url)
                
                # Set the robots.txt content
                robots_content = response.text
                logger.info(f"Robots.txt content for {base_url}:\n{robots_content[:500]}...")
                
                # Parse the content
                robots_parser.read()
                self.robots_cache[base_url] = robots_parser
                
                logger.info(f"Successfully loaded robots.txt for {base_url}")
            else:
                logger.info(f"No robots.txt found for {base_url} (HTTP {response.status_code})")
                self.robots_cache[base_url] = None
                
        except Exception as e:
            logger.warning(f"Failed to load robots.txt from {base_url}: {e}")
            self.robots_cache[base_url] = None
    
    def get_robots_content(self, base_url: str) -> Optional[str]:
        """Get the raw robots.txt content for debugging"""
        try:
            robots_url = urljoin(base_url, "/robots.txt")
            response = self.session.get(robots_url, timeout=10)
            if response.status_code == 200:
                return response.text
        except Exception as e:
            logger.error(f"Error fetching robots.txt content: {e}")
        return None