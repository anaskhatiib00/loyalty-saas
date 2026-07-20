import hashlib
import secrets


INVITATION_TOKEN_BYTES = 32


def generate_invitation_token() -> str:
    """
    Generate a cryptographically secure URL-safe invitation token.

    The raw token must only be returned to the invitation recipient.
    It must never be stored directly in the database.
    """
    return secrets.token_urlsafe(INVITATION_TOKEN_BYTES)


def hash_invitation_token(token: str) -> str:
    """
    Create the deterministic SHA-256 hash stored in the database.
    """
    if not token:
        raise ValueError("Invitation token cannot be empty")

    return hashlib.sha256(token.encode("utf-8")).hexdigest()
