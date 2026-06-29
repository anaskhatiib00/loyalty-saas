import json
from pathlib import Path

from app.credentials.apple_wallet.pass_json import build_pass_json
from app.credentials.apple_wallet.manifest import build_manifest
from app.credentials.apple_wallet.package import create_pkpass_archive
from app.credentials.apple_wallet.schemas import ApplePassContext


class AppleWalletBuilder:

    def build(
        self,
        context: ApplePassContext,
        assets_directory: str,
        output_directory: str,
    ) -> str:

        assets_path = Path(assets_directory)
        output_path = Path(output_directory)

        output_path.mkdir(parents=True, exist_ok=True)

        # Copy assets
        for asset in assets_path.iterdir():
            if asset.is_file():
                (output_path / asset.name).write_bytes(asset.read_bytes())

        # Generate pass.json
        pass_json = build_pass_json(context)

        with open(output_path / "pass.json", "w", encoding="utf-8") as file:
            json.dump(pass_json, file, indent=4)

        # Generate manifest.json
        manifest = build_manifest(str(output_path))

        with open(output_path / "manifest.json", "w", encoding="utf-8") as file:
            json.dump(manifest, file, indent=4)

        # Build pkpass
        return create_pkpass_archive(
            str(output_path),
            str(output_path / "pass.pkpass"),
        )