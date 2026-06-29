import hashlib
from pathlib import Path


def sha1_file(file_path: Path) -> str:
    with file_path.open("rb") as file:
        return hashlib.sha1(file.read()).hexdigest()


def build_manifest(pass_directory: str) -> dict:
    pass_path = Path(pass_directory)

    manifest = {}

    for file_path in pass_path.iterdir():
        if file_path.is_file() and file_path.name != "manifest.json":
            manifest[file_path.name] = sha1_file(file_path)

    return manifest