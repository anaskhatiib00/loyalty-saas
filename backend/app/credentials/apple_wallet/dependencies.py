from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repositories.credential_repository import (
    get_credential_by_provider_reference,
)


def validate_apple_pass_authentication(
    serial_number: str,
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    if authorization is None:
        raise HTTPException(
            status_code=401,
            detail="Missing Authorization header",
        )

    if not authorization.startswith("ApplePass "):
        raise HTTPException(
            status_code=401,
            detail="Invalid Authorization header",
        )

    token = authorization.removeprefix("ApplePass ")

    credential = get_credential_by_provider_reference(
        db,
        serial_number,
    )

    if credential is None:
        raise HTTPException(
            status_code=404,
            detail="Pass not found",
        )

    if credential.authentication_token != token:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token",
        )

    return credential