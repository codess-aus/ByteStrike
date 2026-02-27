import re
from typing import Dict, List


def read_blueprint(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def extract_secrets(content: str) -> List[str]:
    return re.findall(r"\{\* (.*?) \*\}", content)


def categorize_secrets(secrets: List[str]) -> Dict[str, int]:
    categories: Dict[str, int] = {}
    for secret in secrets:
        key = secret.split(":")[0].strip() if ":" in secret else "UNKNOWN"
        categories[key] = categories.get(key, 0) + 1
    return categories


def decode_blueprint_safe(filename: str) -> List[str]:
    try:
        content = read_blueprint(filename)
        return extract_secrets(content)
    except FileNotFoundError:
        print(f"Error: '{filename}' not found.")
        return []
