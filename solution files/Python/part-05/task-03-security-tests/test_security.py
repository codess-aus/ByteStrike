import pytest
from url_validation import validate_url


def test_valid_https_url_passes():
    validate_url("https://raw.githubusercontent.com/microsoft/CopilotAdventures/main/Data/scrolls.txt")


def test_http_url_is_blocked():
    with pytest.raises(ValueError, match="must use HTTPS"):
        validate_url("http://raw.githubusercontent.com/some/path")


def test_unknown_host_is_blocked():
    with pytest.raises(ValueError, match="not in the allowed list"):
        validate_url("https://evil.example.com/payload")
