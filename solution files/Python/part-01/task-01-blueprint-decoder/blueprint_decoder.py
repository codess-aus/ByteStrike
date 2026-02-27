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

# Test the decoder
if __name__ == "__main__":
    secrets = decode_blueprint("blueprint-data.txt")
    print(f"Found {len(secrets)} secret(s):")
    for i, secret in enumerate(secrets, 1):
        print(f"{i}. {secret}")
