import tempfile
from pathlib import Path

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.settings import settings
from app.credentials.apple_wallet.builder import AppleWalletBuilder
from app.credentials.apple_wallet.schemas import ApplePassContext
from app.repositories.credential_repository import get_credential_by_provider_reference
from app.repositories.customer_repository import get_customer_by_id
from app.repositories.loyalty_card_repository import get_loyalty_card_by_customer_id


def generate_apple_wallet_pass_use_case(
    db: Session,
    serial_number: str,
) -> str:
    credential = get_credential_by_provider_reference(db, serial_number)

    if not credential:
        raise HTTPException(status_code=404, detail="Pass not found")

    loyalty_card = credential.loyalty_card

    if not loyalty_card:
        raise HTTPException(status_code=404, detail="Loyalty card not found")

    customer = loyalty_card.customer

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    customer_name = f"{customer.first_name} {customer.last_name or ''}".strip()

    context = ApplePassContext(
        serial_number=credential.provider_reference,
        authentication_token=credential.authentication_token or "missing-token",
        team_identifier=settings.APPLE_TEAM_IDENTIFIER,
        pass_type_identifier=settings.APPLE_PASS_TYPE_IDENTIFIER,
        organization_name=customer.business.name,
        description=f"{customer.business.name} Loyalty Card",
        logo_text=customer.business.name,
        card_number=loyalty_card.card_number,
        public_id=loyalty_card.public_id,
        customer_name=customer_name,
        business_name=customer.business.name,
        current_progress=customer.current_progress,
    )

    temp_output = Path(tempfile.gettempdir()) / f"{serial_number}.pkpass"

    builder = AppleWalletBuilder()

    return builder.build(
        context=context,
        assets_directory="assets/apple_wallet",
        output_path=str(temp_output),
        require_signature=False,
    )