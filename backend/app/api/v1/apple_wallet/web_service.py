from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.application.use_cases.generate_apple_wallet_pass import (
    generate_apple_wallet_pass_use_case,
)
from app.db.database import get_db


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