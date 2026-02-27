import re

# Function to read a blueprint file and extract all secrets marked between {* and *}
# Example: League Blueprint contains {* AGENT_CODENAME: SHADOWMIND *}
# Should extract: "AGENT_CODENAME: SHADOWMIND" (without the markers)
# Uses regex pattern to find all occurrences
# Returns a list of extracted secrets
def decode_blueprint(filename):
    with open(filename, "r") as file:
        content = file.read()

    # Use regex to find all secrets between {* and *}
    pattern = r"\{\* (.*?) \*\}"
    secrets = re.findall(pattern, content)
    return secrets


# Enhanced version with error handling
# If file doesn't exist, return an empty list and print an error message
def decode_blueprint_safe(filename):
    # TODO: Add try-except to catch FileNotFoundError
    # TODO: If file doesn't exist, print error and return empty list
    # TODO: Otherwise, call decode_blueprint and return the secrets
    pass


if __name__ == "__main__":
    # Test error handling
    secrets = decode_blueprint_safe("nonexistent.txt")
    print(f"Found {len(secrets)} secrets")

    # Test normal operation
    secrets = decode_blueprint_safe("blueprint-data.txt")
    print(f"Found {len(secrets)} secrets")
