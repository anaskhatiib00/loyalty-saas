from sqlalchemy.orm import Session

from app.application.use_cases.issue_apple_wallet_credential import (
    issue_apple_wallet_credential_use_case,
)
from app.application.use_cases.issue_google_wallet_credential import (
    issue_google_wallet_credential_use_case,
)
from app.models.user import User
from app.wallet.base import BaseWalletProvider


class AppleWalletProvider(BaseWalletProvider):

    def issue(self, db: Session, current_user: User, customer_id: int):
        return issue_apple_wallet_credential_use_case(
            db=db,
            current_user=current_user,
            customer_id=customer_id,
        )


class GoogleWalletProvider(BaseWalletProvider):

    def issue(self, db: Session, current_user: User, customer_id: int):
        return issue_google_wallet_credential_use_case(
            db=db,
            current_user=current_user,
            customer_id=customer_id,
        )