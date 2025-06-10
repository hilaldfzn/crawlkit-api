import hashlib
import uuid
from datetime import datetime
from typing import Any, Dict, List
import json

def generate_unique_id() -> str:
    """Generate a unique identifier"""
    return str(uuid.uuid4())

def hash_string(text: str) -> str:
    """Generate SHA256 hash of a string"""
    return hashlib.sha256(text.encode()).hexdigest()

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    # Remove invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename.strip()

def format_timestamp(dt: datetime) -> str:
    """Format datetime to ISO string"""
    return dt.isoformat()

def safe_json_loads(json_str: str) -> Dict[str, Any]:
    """Safely load JSON string"""
    try:
        return json.loads(json_str) if json_str else {}
    except (json.JSONDecodeError, TypeError):
        return {}

def safe_json_dumps(data: Any) -> str:
    """Safely dump data to JSON string"""
    try:
        return json.dumps(data, default=str)
    except (TypeError, ValueError):
        return "{}"

def extract_domain(url: str) -> str:
    """Extract domain from URL"""
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc
    except Exception:
        return ""

def calculate_success_rate(successful: int, total: int) -> float:
    """Calculate success rate percentage"""
    if total == 0:
        return 0.0
    return (successful / total) * 100

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."