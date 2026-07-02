import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.application.use_cases.generate_apple_wallet_pass import (
    generate_apple_wallet_pass_use_case,
)
from app.db.database import get_db
from app.repositories.credential_repository import (
    get_credential_by_provider_reference,
)
from app.repositories.apple_wallet_registration_repository import (
    create_registration,
    delete_registration,
    get_registration,
    get_registrations_by_device,
)
from app.schemas.apple_wallet import AppleWalletRegistrationRequest

logger = logging.getLogger(__name__)


class AppleWalletLogRequest(BaseModel):
    logs: List[str]

router = APIRouter(
    prefix="/v1",
    tags=["Apple Wallet"],
)


@router.get("/passes/{pass_type_identifier}/{serial_number}")
def get_wallet_pass(
    pass_type_identifier: str,
    serial_number: str,
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
    status_code=status.HTTP_201_CREATED,
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
        return {}

    create_registration(
        db=db,
        credential_id=credential.id,
        device_library_identifier=device_library_identifier,
        push_token=registration_data.pushToken,
    )

    return {}


@router.delete(
    "/devices/{device_library_identifier}/registrations/{pass_type_identifier}/{serial_number}",
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

    return {}


@router.get(
    "/devices/{device_library_identifier}/registrations/{pass_type_identifier}",
)
def get_updated_passes(
    device_library_identifier: str,
    pass_type_identifier: str,
    passesUpdatedSince: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    registrations = get_registrations_by_device(
        db=db,
        device_library_identifier=device_library_identifier,
    )

    serial_numbers = [
        registration.credential.provider_reference
        for registration in registrations
    ]

    return {
        "lastUpdated": "",
        "serialNumbers": serial_numbers,
    }


@router.post("/log")
def wallet_log(log_request: AppleWalletLogRequest):
    for message in log_request.logs:
        logger.info(f"Apple Wallet: {message}")

    return {}