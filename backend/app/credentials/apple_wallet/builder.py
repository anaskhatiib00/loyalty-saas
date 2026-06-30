import json
import shutil
import tempfile
from pathlib import Path

from app.credentials.apple_wallet.pass_json import build_pass_json
from app.credentials.apple_wallet.manifest import build_manifest
from app.credentials.apple_wallet.package import create_pkpass_archive
from app.credentials.apple_wallet.schemas import ApplePassContext
from app.credentials.apple_wallet.signer import (
    AppleWalletSigner,
    AppleWalletSigningError,
)


class AppleWalletBuilder:

    def build(
        self,
        context: ApplePassContext,
        assets_directory: str,
        output_path: str,
        require_signature: bool = False,
    ) -> str:
        assets_path = Path(assets_directory)
        final_output_path = Path(output_path)

        final_output_path.parent.mkdir(parents=True, exist_ok=True)

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            for asset in assets_path.iterdir():
                if asset.is_file():
                    shutil.copy(asset, temp_path / asset.name)

            pass_json = build_pass_json(context)

            with open(temp_path / "pass.json", "w", encoding="utf-8") as file:
                json.dump(pass_json, file, indent=4)

            manifest = build_manifest(str(temp_path))

            manifest_path = temp_path / "manifest.json"

            with open(manifest_path, "w", encoding="utf-8") as file:
                json.dump(manifest, file, indent=4)

            signature_path = temp_path / "signature"

            try:
                signer = AppleWalletSigner()
                signer.sign_manifest(
                    manifest_path=str(manifest_path),
                    output_signature_path=str(signature_path),
                )
            except AppleWalletSigningError:
                if require_signature:
                    raise

            create_pkpass_archive(
                str(temp_path),
                str(final_output_path),
            )

        return str(final_output_path)