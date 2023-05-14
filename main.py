"""Main, please set environment variable 'MERRIAM_WEBSTER_DICTIONARY_KEY' first."""
import logging
import os
from collections.abc import Generator
from pathlib import Path

from merriam_api_parser._io import Reader, Writer
from merriam_api_parser._requset_resopnse import MerriamWebsterAPI


def init_request_response() -> MerriamWebsterAPI:
    """Initialize MerriamWebsterAPI object."""
    key_name: str = "MERRIAM_WEBSTER_DICTIONARY_KEY"
    dict_key: str | None = os.getenv(key_name)
    if dict_key is None:
        msg: str = f"Please set environment variable {key_name} first"
        raise ValueError(msg)

    return MerriamWebsterAPI(dict_key)


def get_user_input() -> str:
    """Get user input as a string."""
    return input("Please input a word or a path: ")


def process_user_input(user_input: str) -> str | Path:
    """Determine if user input is a word or a path."""
    if user_input == "-d" or "/" in user_input:
        try:
            return get_path(user_input)
        except Exception as error:  # noqa: BLE001
            msg = f"Invalid path: {error}"
            raise ValueError(msg) from error
    return user_input  # single word


def get_path(user_input: str) -> Path:
    """Get path from user input."""
    return Path("data/md/") if user_input == "-d" else Path(user_input)


def get_words(path: Path) -> Generator[str, None, None]:
    """Get words from file."""
    reader = Reader(path)
    yield from reader.get_md_names()


def process_word(request_response: MerriamWebsterAPI, word: str) -> tuple[str, str]:
    """Process a single word and return the response."""
    try:
        logging.info("Getting response for %s", word)
        response = request_response.parse_response(word)
        logging.info("Got response for %s", word)
    # TODO: Specify more specific exception type
    except Exception as error:
        msg: str = f"Failed to get response for {word}: {error}"
        logging.exception(msg)
        response = ""
    return word, response


# Performance improvement
# TODO: Change write and read for single word, not treat as a dict
# TODO: Change to async
def write_to_md(path: Path, word: str, response: str) -> None:
    """Write response to md file."""
    writer = Writer(path / f"{word}.md")
    writer.write(response)


def format_md(path: Path) -> None:
    """Format md file."""
    md_format: str = f"markdownlint {path}/*.md -f"
    os.system(md_format)  # noqa: S605


def main() -> None:
    """Run."""
    request_response: MerriamWebsterAPI = init_request_response()
    user_input = process_user_input(get_user_input())

    if isinstance(user_input, Path):
        path: Path = user_input
        for word, response in (
            process_word(request_response, word) for word in get_words(path)
        ):
            write_to_md(path, word, response)

    elif isinstance(user_input, str):
        path = Path("data/md/")
        word, response = process_word(request_response, user_input)
        write_to_md(path, word, response)

    format_md(path)


def configure_logging() -> None:
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler("api_parser.log", mode="a"),
            logging.StreamHandler(),
        ],
    )


if __name__ == "__main__":
    configure_logging()  # configure logging before running main function
    main()
