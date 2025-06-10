from bs4 import BeautifulSoup
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

class DataExtractor:
    def __init__(self):
        self.soup = None
    
    def extract_data(self, html: str, url: str, rules: Dict[str, str]) -> Dict[str, Any]:
        """Extract data from HTML using CSS selectors"""
        try:
            self.soup = BeautifulSoup(html, 'html.parser')
            extracted = {"url": url, "data": {}, "error": None}
            
            for field, selector in rules.items():
                try:
                    extracted["data"][field] = self._extract_field(selector)
                except Exception as e:
                    logger.error(f"Error extracting field '{field}' from {url}: {e}")
                    extracted["data"][field] = None
            
            return extracted
            
        except Exception as e:
            logger.error(f"Error parsing HTML from {url}: {e}")
            return {"url": url, "data": {}, "error": str(e)}
    
    def _extract_field(self, selector: str) -> Any:
        """Extract a single field using CSS selector"""
        elements = self.soup.select(selector)
        
        if not elements:
            return None
        
        if len(elements) == 1:
            element = elements[0]
            # Try to get text content, or href for links, or src for images
            if element.name == 'a' and element.get('href'):
                return {
                    'text': element.get_text().strip(),
                    'href': element.get('href')
                }
            elif element.name == 'img' and element.get('src'):
                return {
                    'alt': element.get('alt', '').strip(),
                    'src': element.get('src')
                }
            else:
                return element.get_text().strip()
        else:
            # Multiple elements found
            return [self._extract_single_element(elem) for elem in elements]
    
    def _extract_single_element(self, element) -> Any:
        """Extract data from a single element"""
        if element.name == 'a' and element.get('href'):
            return {
                'text': element.get_text().strip(),
                'href': element.get('href')
            }
        elif element.name == 'img' and element.get('src'):
            return {
                'alt': element.get('alt', '').strip(),
                'src': element.get('src')
            }
        else:
            return element.get_text().strip()