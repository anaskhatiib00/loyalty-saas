from pathlib import Path

from app.core.settings import settings


class AppleWalletSigningError(Exception):
    pass


class AppleWalletSigner:
    def __init__(self):
        self.wwdr_cert_path = settings.APPLE_WWDR_CERT_PATH
        self.signer_cert_path = settings.APPLE_SIGNER_CERT_PATH
        self.signer_key_path = settings.APPLE_SIGNER_KEY_PATH

    def validate_certificates(self):
        required_paths = [
            self.wwdr_cert_path,
            self.signer_cert_path,
            self.signer_key_path,
        ]

        for cert_path in required_paths:
            if not cert_path or not Path(cert_path).exists():
                raise AppleWalletSigningError(
                    "Apple Wallet certificate not configured."
                )

    def sign_manifest(self, manifest_path: str, output_signature_path: str):
        self.validate_certificates()

        raise AppleWalletSigningError(
            "Apple Wallet signing is not available until certificates are configured."
        )