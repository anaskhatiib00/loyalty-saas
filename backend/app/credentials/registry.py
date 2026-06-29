from app.core.enums import CredentialProvider

from app.credentials.providers.apple_provider import AppleWalletProvider
from app.credentials.providers.google_provider import GoogleWalletProvider
from app.credentials.providers.qr_provider import QRProvider


class CredentialProviderRegistry:
    providers = {
        CredentialProvider.APPLE_WALLET: AppleWalletProvider(),
        CredentialProvider.GOOGLE_WALLET: GoogleWalletProvider(),
        CredentialProvider.QR: QRProvider(),
    }

    @classmethod
    def get_provider(cls, provider: CredentialProvider):
        return cls.providers[provider]