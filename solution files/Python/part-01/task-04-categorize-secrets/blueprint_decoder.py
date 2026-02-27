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
    print("DECODED SECRETS REPORT".center(50))
    print(separator)
    print(f"Total secrets found: {len(secrets)}\n")

    for i, secret in enumerate(secrets, 1):
        print(f"  [{i:2d}] {secret}")

    print("\n" + separator + "\n")


# Function to categorize secrets by their type (word before the colon)
def categorize_secrets(secrets):
    categories = {}
    for secret in secrets:
        if ":" in secret:
            category = secret.split(":")[0].strip()
        else:
            category = "UNCLASSIFIED"

        if category not in categories:
            categories[category] = 0
        categories[category] += 1

    return categories


if __name__ == "__main__":
    secrets = decode_blueprint_safe("blueprint-data.txt")
    display_secrets_report(secrets)

    categories = categorize_secrets(secrets)
    print("\nSecret Categories:")
    for category, count in sorted(categories.items()):
        print(f"  {category}: {count}")
