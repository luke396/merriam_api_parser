"""Main, please set environment variable "MERRIAM_WEBSTER_DICTIONARY_KEY" first."""
import os
from pathlib import Path

from merriam_api_parser._io import Reader, Writer
from merriam_api_parser._requset_resopnse import RequestResponse


def get_key() -> RequestResponse:
    """Get key from environment variable."""
    key_name = "MERRIAM_WEBSTER_DICTIONARY_KEY"
    dict_key: str | None = os.getenv(key_name)
    if dict_key is None:
        msg: str = f"Please set environment variable {key_name} first"
        raise ValueError(msg)

    return RequestResponse(dict_key)


DICT_REQUESTER: RequestResponse = get_key()


def get_words(path: Path) -> list[str]:
    """Get words from file."""
    reader = Reader(path)
    return reader.get_md_names()


def main() -> None:
    """Get path and run."""
    path_input: str = input("Please input path or -d, default is data/md/:\n")
    path: Path = Path(path_input) if path_input != "-d" else Path("data/md/")

    words: list[str] = get_words(path)
    word_responses: dict[str, str] = {}
    for word in words:
        response: str = DICT_REQUESTER.parse_resonse(word)
        word_responses[word] = response

    writer = Writer(path)
    writer.write(word_responses)

    md_foramt: str = f"markdownlint {path}/*.md -f"
    os.system(md_foramt)  # noqa: S605


if __name__ == "__main__":
    main()
