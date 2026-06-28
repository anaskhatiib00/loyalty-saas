import secrets
import string
import uuid


CARD_ALPHABET = string.ascii_uppercase + string.digits


def generate_public_id() -> str:
    return str(uuid.uuid4())


def generate_card_number(prefix: str = "LOY") -> str:
    clean_prefix = "".join(char for char in prefix.upper() if char.isalnum())

    if not clean_prefix:
        clean_prefix = "LOY"

    clean_prefix = clean_prefix[:6]

    first_block = "".join(secrets.choice(CARD_ALPHABET) for _ in range(4))
    second_block = "".join(secrets.choice(CARD_ALPHABET) for _ in range(4))

    return f"{clean_prefix}-{first_block}-{second_block}"