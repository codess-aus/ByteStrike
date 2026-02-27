import json
import logging
from datetime import datetime, timezone


def log_mission_result(url: str, secrets_count: int, success: bool, reason: str = "") -> None:
    """Emit a structured audit log entry. Never log secret content."""
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": url,
        "secrets_recovered": secrets_count,
        "success": success,
        "reason": reason,
    }
    logging.info(json.dumps(entry))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    log_mission_result("https://raw.githubusercontent.com/...", secrets_count=5, success=True)
