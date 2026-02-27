from blueprint_decoder import extract_secrets, categorize_secrets


def test_extract_secrets_finds_all():
    content = "data {* SECRET_ONE *} more {* KEY: VALUE *} end"
    assert extract_secrets(content) == ["SECRET_ONE", "KEY: VALUE"]


def test_extract_secrets_no_matches():
    assert extract_secrets("no secrets here") == []


def test_extract_secrets_empty_string():
    assert extract_secrets("") == []


def test_categorize_secrets_by_prefix():
    secrets = [
        "AGENT_CODENAME: SHADOWMIND",
        "VAULT_ACCESS_CODE: DELTA-7",
        "AGENT_CODENAME: GHOSTFIRE",
    ]
    result = categorize_secrets(secrets)
    assert result == {"AGENT_CODENAME": 2, "VAULT_ACCESS_CODE": 1}


def test_categorize_secrets_no_colon():
    assert categorize_secrets(["SECURE_COMMS_PROTOCOL"]) == {"UNKNOWN": 1}


def test_categorize_secrets_empty():
    assert categorize_secrets([]) == {}
