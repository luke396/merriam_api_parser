"""Main, please set environment variable "MERRIAM_WEBSTER_DICTIONARY_KEY" first."""
import logging
import os
from pathlib import Path

from merriam_api_parser._io import Reader, Writer
from merriam_api_parser._requset_resopnse import RequestResponse


def init_request_response() -> RequestResponse:
    """Init RequestResponse, get key from environment variable."""
    key_name = "MERRIAM_WEBSTER_DICTIONARY_KEY"
    dict_key: str | None = os.getenv(key_name)
    if dict_key is None:
        msg: str = f"Please set environment variable {key_name} first"
        raise ValueError(msg)

    return RequestResponse(dict_key)


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

    request_response: RequestResponse = init_request_response()
    for word in words:
        try:
            logging.info("Get response for %s", word)
            response: str = request_response.parse_resonse(word)
        except Exception:
            logging.exception("Get response for %s failed", word)
            continue
        word_responses[word] = response

    # TODO: change write and read for single, not list
    # TODO: change to async
    writer = Writer(path)
    writer.write(word_responses)

    md_foramt: str = f"markdownlint {path}/*.md -f"
    os.system(md_foramt)  # noqa: S605


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
