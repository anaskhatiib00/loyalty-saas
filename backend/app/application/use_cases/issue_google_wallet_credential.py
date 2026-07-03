from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.enums import CredentialProvider, CredentialStatus
from app.core.settings import settings
from app.credentials.google_wallet.schemas import GoogleWalletContext
from app.credentials.google_wallet.object_builder import build_google_loyalty_object
from app.models.credential import Credential
from app.models.user import User
from app.repositories.business_repository import get_business_by_owner_id
from app.repositories.credential_repository import (
    create_credential,
    update_credential,
    get_credential_by_card_and_provider,
)
from app.repositories.customer_repository import get_customer_by_id
from app.repositories.loyalty_card_repository import get_loyalty_card_by_customer_id
from app.utils.tokens import generate_authentication_token


def issue_google_wallet_credential_use_case(
    db: Session,
    current_user: User,
    customer_id: int,
):
    business = get_business_by_owner_id(db, current_user.id)

    if not business:
        raise HTTPException(status_code=404, detail="Business profile not found")

    customer = get_customer_by_id(db, customer_id)

    if not customer or customer.business_id != business.id:
        raise HTTPException(status_code=404, detail="Customer not found")

    loyalty_card = get_loyalty_card_by_customer_id(db, customer.id)

    if not loyalty_card:
        raise HTTPException(status_code=404, detail="Loyalty card not found")

    existing_credential = get_credential_by_card_and_provider(
        db=db,
        loyalty_card_id=loyalty_card.id,
        provider=CredentialProvider.GOOGLE_WALLET,
    )

    if existing_credential:
        return existing_credential

    if not settings.GOOGLE_WALLET_ISSUER_ID:
        raise HTTPException(
            status_code=500,
            detail="Google Wallet issuer ID is not configured",
        )

    customer_name = f"{customer.first_name} {customer.last_name or ''}".strip()

    context = GoogleWalletContext(
        issuer_id=settings.GOOGLE_WALLET_ISSUER_ID,
        class_suffix=settings.GOOGLE_WALLET_CLASS_SUFFIX,
        business_name=business.name,
        customer_name=customer_name,
        card_number=loyalty_card.card_number,
        public_id=loyalty_card.public_id,
        current_progress=customer.current_progress,
    )

    google_object = build_google_loyalty_object(context)

    credential = Credential(
        loyalty_card_id=loyalty_card.id,
        provider=CredentialProvider.GOOGLE_WALLET,
        provider_reference=google_object["id"],
        authentication_token=generate_authentication_token(),
        status=CredentialStatus.ACTIVE,
    )

    return create_credential(db, credential)