import re
from typing import Dict, List


def read_blueprint(filename: str) -> str:
    """Read and return the raw content of a blueprint file."""
    with open(filename, "r") as f:
        return f.read()


def extract_secrets(content: str) -> List[str]:
    """Extract all secrets marked between {* and *} from content."""
    return re.findall(r"\{\* (.*?) \*\}", content)


def categorize_secrets(secrets: List[str]) -> Dict[str, int]:
    """Count secrets by their category prefix (text before the first colon)."""
    categories: Dict[str, int] = {}
    for secret in secrets:
        key = secret.split(":")[0].strip() if ":" in secret else "UNKNOWN"
        categories[key] = categories.get(key, 0) + 1
    return categories


def decode_blueprint_safe(filename: str) -> List[str]:
    """Full pipeline: read file safely and extract secrets."""
    try:
        content = read_blueprint(filename)
        return extract_secrets(content)
    except FileNotFoundError:
        print(f"Error: '{filename}' not found.")
        return []
