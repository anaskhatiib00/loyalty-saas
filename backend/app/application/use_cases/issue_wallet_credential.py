from sqlalchemy.orm import Session

from app.core.enums import CredentialProvider
from app.models.user import User
from app.wallet.registry import WalletProviderRegistry


def issue_wallet_credential_use_case(
    db: Session,
    current_user: User,
    customer_id: int,
    provider: CredentialProvider,
):
    wallet_provider = WalletProviderRegistry.get_provider(provider)

    return wallet_provider.issue(
        db=db,
        current_user=current_user,
        customer_id=customer_id,
    )