import os
import shutil
from pathlib import Path


def move_files_to_another_directory(
    source_directory: Path, target_directory: Path
) -> None:
    if os.path.exists(f"{target_directory}"):
        shutil.rmtree(Path(f"{target_directory}"))

    shutil.copytree(src=Path(source_directory), dst=Path(target_directory))
