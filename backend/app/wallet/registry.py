from fastapi import HTTPException

from app.core.enums import CredentialProvider
from app.wallet.providers import AppleWalletProvider, GoogleWalletProvider


class WalletProviderRegistry:
    providers = {
        CredentialProvider.APPLE_WALLET: AppleWalletProvider(),
        CredentialProvider.GOOGLE_WALLET: GoogleWalletProvider(),
    }

    @classmethod
    def get_provider(cls, provider: CredentialProvider):
        wallet_provider = cls.providers.get(provider)

        if not wallet_provider:
            raise HTTPException(
                status_code=400,
                detail="Unsupported wallet provider",
            )

        return wallet_provider