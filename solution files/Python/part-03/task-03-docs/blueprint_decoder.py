import re
from typing import Dict, List


def read_blueprint(filename: str) -> str:
    """
    Read and return the raw content of a blueprint file.

    Args:
        filename: Path to the blueprint file.

    Returns:
        The file contents as a string.

    Raises:
        FileNotFoundError: If the file does not exist.

    Example:
        >>> content = read_blueprint("blueprint-data.txt")
        >>> isinstance(content, str)
        True
    """
    with open(filename, "r") as f:
        return f.read()


def extract_secrets(content: str) -> List[str]:
    """
    Extract all secrets marked between {* and *} delimiters from a string.

    Searches the given content for all occurrences of the pattern {* ... *}
    and returns the text found between each pair of markers.

    Args:
        content: The raw text to search. May contain zero or more secret markers.

    Returns:
        A list of extracted secret strings, in the order they appear.
        Returns an empty list if no markers are found.

    Example:
        >>> extract_secrets("data {* VAULT_CODE: DELTA-7 *} and {* PROTOCOL *}")
        ['VAULT_CODE: DELTA-7', 'PROTOCOL']
    """
    return re.findall(r"\{\* (.*?) \*\}", content)


def categorize_secrets(secrets: List[str]) -> Dict[str, int]:
    """
    Count secrets by their category prefix (text before the first colon).

    Args:
        secrets: List of secret strings.

    Returns:
        A mapping of category name to count.

    Example:
        >>> categorize_secrets(["AGENT: ONE", "AGENT: TWO", "VAULT: X"])
        {'AGENT': 2, 'VAULT': 1}
    """
    categories: Dict[str, int] = {}
    for secret in secrets:
        key = secret.split(":")[0].strip() if ":" in secret else "UNKNOWN"
        categories[key] = categories.get(key, 0) + 1
    return categories


def decode_blueprint_safe(filename: str) -> List[str]:
    """
    Full pipeline: read a file safely and extract secrets.

    Args:
        filename: Path to the blueprint file.

    Returns:
        A list of extracted secrets, or an empty list if the file is missing.
    """
    try:
        content = read_blueprint(filename)
        return extract_secrets(content)
    except FileNotFoundError:
        print(f"Error: '{filename}' not found.")
        return []
