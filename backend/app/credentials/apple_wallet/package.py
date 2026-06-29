import zipfile
from pathlib import Path


def create_pkpass_archive(pass_directory: str, output_path: str) -> str:
    pass_path = Path(pass_directory)
    output = Path(output_path)

    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as pkpass:
        for file_path in pass_path.iterdir():
            if file_path.is_file():
                pkpass.write(file_path, arcname=file_path.name)

    return str(output)