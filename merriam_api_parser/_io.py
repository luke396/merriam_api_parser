import os
from collections.abc import Generator
from pathlib import Path


class Reader:
    """Read a directory or single file."""

    def __init__(self, path: Path) -> None:
        if path.is_dir():
            self._file_names: list[str] = [
                entry.name for entry in os.scandir(path) if entry.name.endswith(".md")
            ]
        else:
            self._file_names = [path.name]

    def get_md_names(self) -> list[str]:
        """Return md names wanted."""
        return [Path(file_name).stem for file_name in self._file_names]

    def get_words(self) -> Generator[str, None, None]:
        """Get words from file."""
        yield from self.get_md_names()


class Writer:
    """Write md-formated text to file."""

    def __init__(self, out_path: Path) -> None:
        self.out_path: Path = out_path

    def write(self, response: str) -> None:
        """Write md-formated text to file."""
        with self.out_path.open("w", encoding="UTF-8") as file:
            file.write(response)


class MdFormatter:
    """Format md file."""

    def __init__(self, path: Path) -> None:
        self.path: Path = path

    def md_format(self) -> None:
        """Format md file."""
        md_format: str = f"markdownlint {self.path}/*.md -f"
        os.system(md_format)  # noqa: S605
