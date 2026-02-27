from typing import Any, Dict, List


def transform(data: List[Dict[str, Any]]) -> List[str]:
    # Extract the 'name' field from each dictionary and return as a list of strings
    return [item["name"] for item in data]
