from app.credentials.base import BaseCredentialProvider


class GoogleWalletProvider(BaseCredentialProvider):

    def issue(self, loyalty_card):
        raise NotImplementedError("Google Wallet provider is not implemented yet")

    def update(self, credential):
        raise NotImplementedError("Google Wallet provider is not implemented yet")

    def revoke(self, credential):
        raise NotImplementedError("Google Wallet provider is not implemented yet")