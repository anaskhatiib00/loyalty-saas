from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.application.use_cases.issue_apple_wallet_credential import (
    issue_apple_wallet_credential_use_case,
)
from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.credential import CredentialResponse

from app.application.use_cases.issue_google_wallet_credential import (
    issue_google_wallet_credential_use_case,
)

from app.application.use_cases.issue_wallet_credential import (
    issue_wallet_credential_use_case,
)
from app.core.enums import CredentialProvider


router = APIRouter(
    prefix="/credentials",
    tags=["Credentials"],
)


@router.post(
    "/apple-wallet/customer/{customer_id}",
    response_model=CredentialResponse,
)
def issue_apple_wallet_credential(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return issue_apple_wallet_credential_use_case(db, current_user, customer_id)


@router.post(
    "/google-wallet/customer/{customer_id}",
    response_model=CredentialResponse,
)
def issue_google_wallet_credential(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return issue_google_wallet_credential_use_case(db, current_user, customer_id)


@router.post(
    "/{provider}/customer/{customer_id}",
    response_model=CredentialResponse,
)
def issue_wallet_credential(
    provider: CredentialProvider,
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return issue_wallet_credential_use_case(
        db=db,
        current_user=current_user,
        customer_id=customer_id,
        provider=provider,
    )