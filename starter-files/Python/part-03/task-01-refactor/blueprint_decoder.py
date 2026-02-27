def decode_blueprint(filename):
    try:
        with open(filename, "r") as f:
            content = f.read()
        import re
        secrets = re.findall(r"\{\* (.*?) \*\}", content)
        print("=" * 40)
        print("DECODED SECRETS REPORT")
        print("=" * 40)
        print(f"Found {len(secrets)} secret(s):\n")
        for i, s in enumerate(secrets, 1):
            print(f"{i}. {s}")
        print("=" * 40)
        cats = {}
        for s in secrets:
            key = s.split(":")[0].strip() if ":" in s else "UNKNOWN"
            cats[key] = cats.get(key, 0) + 1
        return cats
    except FileNotFoundError:
        print(f"Error: '{filename}' not found.")
        return {}
