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


# Function to format and display secrets in a professional report
# Includes header, separator lines, numbered list, and footer
def display_secrets_report(secrets):
    separator = "=" * 50
    print("\n" + separator)
    print("🔐 DECODED SECRETS REPORT".center(50))
    print(separator)
    print(f"Total secrets found: {len(secrets)}\n")

    for i, secret in enumerate(secrets, 1):
        print(f"  [{i:2d}] {secret}")

    print("\n" + separator + "\n")


if __name__ == "__main__":
    secrets = decode_blueprint_safe("blueprint-data.txt")
    display_secrets_report(secrets)
