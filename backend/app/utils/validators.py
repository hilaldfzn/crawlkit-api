import re
from urllib.parse import urlparse
from typing import List

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.match(pattern, email) is not None

def validate_url(url: str) -> bool:
    """Validate URL format"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def validate_urls(urls: List[str]) -> List[str]:
    """Validate a list of URLs and return valid ones"""
    return [url for url in urls if validate_url(url)]

def validate_css_selector(selector: str) -> bool:
    """Basic CSS selector validation"""
    if not selector or not isinstance(selector, str):
        return False
    
    # Check for basic CSS selector patterns
    valid_patterns = [
        r'^[a-zA-Z][a-zA-Z0-9_-]*',                          # element selector
        r'^\.[a-zA-Z][a-zA-Z0-9_-]*',                        # class selector
        r'^#[a-zA-Z][a-zA-Z0-9_-]*',                         # id selector
        r'^[a-zA-Z][a-zA-Z0-9_-]*\.[a-zA-Z][a-zA-Z0-9_-]*',  # element.class
    ]
    
    return any(re.match(pattern, selector.strip()) for pattern in valid_patterns)

def validate_extraction_rules(rules: dict) -> bool:
    """Validate extraction rules dictionary"""
    if not isinstance(rules, dict) or not rules:
        return False
    
    for field_name, selector in rules.items():
        if not isinstance(field_name, str) or not field_name.strip():
            return False
        if not validate_css_selector(selector):
            return False
    
    return True