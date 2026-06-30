import secrets


def generate_authentication_token() -> str:
    return secrets.token_hex(32)