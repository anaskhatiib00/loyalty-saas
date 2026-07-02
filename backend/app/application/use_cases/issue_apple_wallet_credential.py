from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.enums import CredentialProvider, CredentialStatus
from app.core.settings import settings
from app.credentials.apple_wallet.builder import AppleWalletBuilder
from app.credentials.apple_wallet.schemas import ApplePassContext
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
from app.storage.local_storage import LocalStorageService
from app.utils.tokens import generate_authentication_token


def issue_apple_wallet_credential_use_case(
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
        provider=CredentialProvider.APPLE_WALLET,
    )

    if existing_credential:
        return existing_credential

    authentication_token = generate_authentication_token()
    serial_number = loyalty_card.public_id

    credential = Credential(
        loyalty_card_id=loyalty_card.id,
        provider=CredentialProvider.APPLE_WALLET,
        provider_reference=serial_number,
        authentication_token=authentication_token,
        status=CredentialStatus.PENDING,
    )

    credential = create_credential(db, credential)

    customer_name = f"{customer.first_name} {customer.last_name or ''}".strip()

    context = ApplePassContext(
        serial_number=serial_number,
        authentication_token=authentication_token,
        team_identifier=settings.APPLE_TEAM_IDENTIFIER or "DEMO_TEAM",
        pass_type_identifier=settings.APPLE_PASS_TYPE_IDENTIFIER
        or "pass.com.demo.loyalty",
        organization_name=business.name,
        description=f"{business.name} Loyalty Card",
        logo_text=business.name,
        card_number=loyalty_card.card_number,
        public_id=loyalty_card.public_id,
        customer_name=customer_name,
        business_name=business.name,
        current_progress=customer.current_progress,
    )

    builder = AppleWalletBuilder()

    generated_pass_path = builder.build(
        context=context,
        assets_directory="assets/apple_wallet",
        output_path=f"generated_passes/{loyalty_card.public_id}.pkpass",
        require_signature=False,
    )

    storage = LocalStorageService()

    stored_path = storage.save_file(
        source_path=generated_pass_path,
        destination_path=f"apple_wallet/{loyalty_card.public_id}.pkpass",
    )

    credential.storage_path = stored_path
    credential.status = CredentialStatus.ACTIVE

    return update_credential(db, credential)