import logging
from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.application.use_cases.generate_apple_wallet_pass import (
    generate_apple_wallet_pass_use_case,
)
from app.credentials.apple_wallet.dependencies import (
    validate_apple_pass_authentication,
)
from app.db.database import get_db
from app.repositories.apple_wallet_registration_repository import (
    create_registration,
    delete_registration,
    get_registration,
    get_registrations_by_device_updated_since,
)
from app.repositories.credential_repository import (
    get_credential_by_provider_reference,
)
from app.schemas.apple_wallet import AppleWalletRegistrationRequest


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/v1",
    tags=["Apple Wallet"],
)


class AppleWalletLogRequest(BaseModel):
    logs: List[str]


def parse_apple_timestamp(value: str | None):
    if not value:
        return None

    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


@router.get("/passes/{pass_type_identifier}/{serial_number}")
def get_wallet_pass(
    pass_type_identifier: str,
    serial_number: str,
    credential=Depends(validate_apple_pass_authentication),
    db: Session = Depends(get_db),
):
    pkpass_path = generate_apple_wallet_pass_use_case(
        db=db,
        serial_number=serial_number,
    )

    return FileResponse(
        pkpass_path,
        media_type="application/vnd.apple.pkpass",
        filename="pass.pkpass",
    )


@router.post(
    "/devices/{device_library_identifier}/registrations/{pass_type_identifier}/{serial_number}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def register_device_for_pass(
    device_library_identifier: str,
    pass_type_identifier: str,
    serial_number: str,
    registration_data: AppleWalletRegistrationRequest,
    db: Session = Depends(get_db),
):
    credential = get_credential_by_provider_reference(db, serial_number)

    if not credential:
        raise HTTPException(status_code=404, detail="Pass not found")

    existing_registration = get_registration(
        db=db,
        credential_id=credential.id,
        device_library_identifier=device_library_identifier,
    )

    if existing_registration:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    create_registration(
        db=db,
        credential_id=credential.id,
        device_library_identifier=device_library_identifier,
        push_token=registration_data.pushToken,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "/devices/{device_library_identifier}/registrations/{pass_type_identifier}/{serial_number}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def unregister_device_from_pass(
    device_library_identifier: str,
    pass_type_identifier: str,
    serial_number: str,
    db: Session = Depends(get_db),
):
    credential = get_credential_by_provider_reference(db, serial_number)

    if not credential:
        raise HTTPException(status_code=404, detail="Pass not found")

    registration = get_registration(
        db=db,
        credential_id=credential.id,
        device_library_identifier=device_library_identifier,
    )

    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")

    delete_registration(db, registration)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/devices/{device_library_identifier}/registrations/{pass_type_identifier}",
)
def get_updated_passes(
    device_library_identifier: str,
    pass_type_identifier: str,
    passesUpdatedSince: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    updated_since = parse_apple_timestamp(passesUpdatedSince)

    registrations = get_registrations_by_device_updated_since(
        db=db,
        device_library_identifier=device_library_identifier,
        updated_since=updated_since,
    )

    serial_numbers = [
        registration.credential.provider_reference
        for registration in registrations
    ]

    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    return {
        "lastUpdated": now,
        "serialNumbers": serial_numbers,
    }


@router.post("/log", status_code=status.HTTP_204_NO_CONTENT)
def wallet_log(log_request: AppleWalletLogRequest):
    for message in log_request.logs:
        logger.info(f"Apple Wallet: {message}")

    return Response(status_code=status.HTTP_204_NO_CONTENT)