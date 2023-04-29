"""Reader and writer"""
import os


# TODO: need to support single file or directory
class Reader:
    """Read a directory or single file"""

    def __init__(self, path: str) -> None:
        self._file_mane: list[str] = (
            self._load_file_list(path) if os.path.isdir(path) else [path]
        )

    def _load_file_list(self, dir_path) -> list[str]:
        """Load all md files's name."""
        return [
            file_name for file_name in os.listdir(dir_path) if file_name.endswith(".md")
        ]

    def get_md_names(self, raw: bool) -> list[str]:
        """Return md names wanted

        Args:
            raw (bool): With or without .md

        Returns:
            list[str]
        """
        if raw:
            return self._file_mane

        return [file_name[:-3] for file_name in self._file_mane]


class Writer:
    """Write md-formated text to file"""

    def __init__(self, path: str) -> None:
        self.path: str = path

    def write(self, word_response: dict[str, str]) -> None:
        """Write md-formated text to file

        Args:
            word_response (dict[str, str]): All md text to write\
                                            (contains header, content, etc)
        """
        for word, response in word_response.items():
            with open(f"{self.path}/{word}.md", "w", encoding="UTF-8") as file:
                file.write(response)
