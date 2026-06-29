from app.credentials.base import BaseCredentialProvider


class AppleWalletProvider(BaseCredentialProvider):

    def issue(self, loyalty_card):
        raise NotImplementedError("Apple Wallet provider is not implemented yet")

    def update(self, credential):
        raise NotImplementedError("Apple Wallet provider is not implemented yet")

    def revoke(self, credential):
        raise NotImplementedError("Apple Wallet provider is not implemented yet")