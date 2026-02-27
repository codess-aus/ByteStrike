import re

def decode_blueprint(filename):
    with open(filename, "r") as file:
        content = file.read()

    pattern = r"\{\* (.*?) \*\}"
    secrets = re.findall(pattern, content)
    return secrets


# Enhanced version with error handling
# If file doesn't exist, return an empty list and print an error message
def decode_blueprint_safe(filename):
    try:
        return decode_blueprint(filename)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []


if __name__ == "__main__":
    # Test error handling
    secrets = decode_blueprint_safe("nonexistent.txt")
    print(f"Found {len(secrets)} secrets")

    # Test normal operation
    secrets = decode_blueprint_safe("blueprint-data.txt")
    print(f"Found {len(secrets)} secrets")
