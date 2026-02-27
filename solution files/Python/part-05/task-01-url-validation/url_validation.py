from urllib.parse import urlparse

ALLOWED_HOSTS = {
    "raw.githubusercontent.com",
    "league-blueprints.internal",
}


def validate_url(url: str) -> None:
    """Raise ValueError if the URL's host is not in the allowlist."""
    parsed = urlparse(url)
    if parsed.scheme not in ("https",):
        raise ValueError(f"URL must use HTTPS. Got: {parsed.scheme!r}")
    if parsed.netloc not in ALLOWED_HOSTS:
        raise ValueError(f"Host '{parsed.netloc}' is not in the allowed list.")


if __name__ == "__main__":
    try:
        validate_url(
            "https://raw.githubusercontent.com/microsoft/CopilotAdventures/main/Data/scrolls.txt"
        )
        print("URL is valid")
    except ValueError as e:
        print(f"Blocked: {e}")
