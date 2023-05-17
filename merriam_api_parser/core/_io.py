"""Reader and writer."""
import os
from pathlib import Path


# TODO: support single file or directory
class Reader:
    """Read a directory or single file."""

    def __init__(self, path: Path) -> None:
        self._file_mane: list[str] = (
            self._load_file_list(path) if Path.is_dir(path) else [str(path)]
        )

    def _load_file_list(self, dir_path: Path) -> list[str]:
        """Load all md files's name."""
        return [
            file_name for file_name in os.listdir(dir_path) if file_name.endswith(".md")
        ]

    def get_md_names(self) -> list[str]:
        """Return md names wanted."""
        return [file_name[:-3] for file_name in self._file_mane]


class Writer:
    """Write md-formated text to file."""

    def __init__(self, out_path: Path) -> None:
        self.out_path: Path = out_path

    def write(self, response: str) -> None:
        """Write md-formated text to file."""
        with Path.open(self.out_path, "w", encoding="UTF-8") as file:
            file.write(response)
