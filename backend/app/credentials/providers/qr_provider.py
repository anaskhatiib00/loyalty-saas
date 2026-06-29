from app.credentials.base import BaseCredentialProvider


class QRProvider(BaseCredentialProvider):

    def issue(self, loyalty_card):
        raise NotImplementedError("QR provider is not implemented yet")

    def update(self, credential):
        raise NotImplementedError("QR provider is not implemented yet")

    def revoke(self, credential):
        raise NotImplementedError("QR provider is not implemented yet")