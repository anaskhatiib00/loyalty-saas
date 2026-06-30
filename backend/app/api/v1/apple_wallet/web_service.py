from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repositories.credential_repository import (
    get_credential_by_provider_reference,
)

router = APIRouter(
    prefix="/v1",
    tags=["Apple Wallet"],
)


@router.get(
    "/passes/{pass_type_identifier}/{serial_number}",
)
def get_wallet_pass(
    pass_type_identifier: str,
    serial_number: str,
    db: Session = Depends(get_db),
):
    credential = get_credential_by_provider_reference(
        db,
        serial_number,
    )

    if credential is None:
        raise HTTPException(
            status_code=404,
            detail="Pass not found",
        )

    if not credential.storage_path:
        raise HTTPException(
            status_code=404,
            detail="Pass file not found",
        )

    return FileResponse(
        credential.storage_path,
        media_type="application/vnd.apple.pkpass",
        filename="pass.pkpass",
    )