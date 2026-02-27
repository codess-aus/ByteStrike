import re


def decode_blueprint(filename):
    with open(filename, "r") as file:
        content = file.read()

    pattern = r"\{\* (.*?) \*\}"
    secrets = re.findall(pattern, content)
    return secrets
