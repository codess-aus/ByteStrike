import logging
import re
import time
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

MAX_RETRIES = 3
BASE_DELAY = 1  # seconds


def retrieve_and_decode_blueprint(blueprint_url: str) -> None:
    """Retrieve a blueprint URL and print extracted secrets. Retries up to 3 times."""
    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(blueprint_url, timeout=10)
            response.raise_for_status()
            secrets = re.findall(r"\{\*(.*?)\*\}", response.text)
            for idx, secret in enumerate(secrets, 1):
                print(f"Secret #{idx}: {secret.strip()}")
            return
        except (requests.ConnectionError, requests.Timeout) as e:
            last_error = e
            wait = BASE_DELAY * (2 ** (attempt - 1))
            logging.warning(
                f"Attempt {attempt}/{MAX_RETRIES} failed: {e}. Retrying in {wait}s..."
            )
            time.sleep(wait)
    logging.error(f"All {MAX_RETRIES} attempts failed. Last error: {last_error}")


if __name__ == "__main__":
    blueprint_url = "https://raw.githubusercontent.com/microsoft/CopilotAdventures/main/Data/scrolls.txt"
    retrieve_and_decode_blueprint(blueprint_url)
