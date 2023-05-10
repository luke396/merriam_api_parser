"""Main, please set environment variable 'MERRIAM_WEBSTER_DICTIONARY_KEY' first."""
import logging
import os
from pathlib import Path

from merriam_api_parser._io import Reader, Writer
from merriam_api_parser._requset_resopnse import RequestResponse


def init_request_response() -> RequestResponse:
    """Init RequestResponse, get key from environment variable."""
    key_name: str = "MERRIAM_WEBSTER_DICTIONARY_KEY"
    dict_key: str | None = os.getenv(key_name)
    if dict_key is None:
        msg: str = f"Please set environment variable {key_name} first"
        raise ValueError(msg)

    return RequestResponse(dict_key)


def get_words(path: Path) -> list[str]:
    """Get words from file."""
    reader = Reader(path)
    return reader.get_md_names()


def process_word(request_response: RequestResponse, word: str) -> str:
    """Process a single word and return the response."""
    response: str = ""
    try:
        logging.info("Getting response for %s", word)
        response = request_response.parse_response(word)
        logging.info("Got response for %s", word)
    # TODO: Specify more specific exception type
    except Exception as error:  # pylint: disable=broad-except
        msg: str = f"Failed to get response for {word}: {error}"
        logging.exception(msg)
    return response


def main() -> None:
    """Get path and run."""
    path_input: str = input("Please input path or -d, default is data/md/: ")
    path: Path = Path(path_input) if path_input != "-d" else Path("data/md/")

    words: list[str] = get_words(path)
    word_responses: dict[str, str] = {}

    request_response: RequestResponse = init_request_response()
    for word in words:
        response: str = process_word(request_response, word)
        word_responses[word] = response

    # Performance improvement
    # TODO: Change write and read for single word, not treat as a dict
    # TODO: Change to async
    writer = Writer(path)
    writer.write(word_responses)

    md_format: str = f"markdownlint {path}/*.md -f"
    os.system(md_format)  # noqa: S605


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler("api_parser.log", mode="a"),
            logging.StreamHandler(),
        ],
    )

    main()

# TODO: handle error for `harass`, maybe need parse more sense.
