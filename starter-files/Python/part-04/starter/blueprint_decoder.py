import requests
import re


def retrieve_and_decode_blueprint(blueprint_url):
    """
    Retrieves a classified League blueprint and deciphers it,
    extracting only authentic secrets hidden by The League's tech.
    Secrets are wrapped in {* and *} markers.
    """
    try:
        response = requests.get(blueprint_url, timeout=10)
        response.raise_for_status()

        secret_pattern = re.compile(r"\{\*(.*?)\*\}")
        secrets = secret_pattern.findall(response.text)

        print("=== LEAGUE MISSION REPORT ===")
        if secrets:
            for idx, secret in enumerate(secrets, 1):
                print(f"Secret #{idx}: {secret.strip()}")
        else:
            print("No authentic secrets found. The League's decoys were strong!")

    except Exception as err:
        print(f"[ALERT] Unexpected error: {err}")


# Run the mission
blueprint_url = "https://raw.githubusercontent.com/codess-aus/AI-Assisted-Dev-with-GitHub-Copilot/main/blueprint-data.txt"
retrieve_and_decode_blueprint(blueprint_url)
