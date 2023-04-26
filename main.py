"""Main"""
import os
from typing import Optional

from merriam_api_parser._io import MdReader, Writer
from merriam_api_parser._requset_resopnse import RequestResponse

DICT_KEY: Optional[str] = os.getenv("MERRIAM_WEBSTER_DICTIONARY_KEY")
DICT_REQUESTER = RequestResponse(DICT_KEY)  # type: ignore


def main() -> None:
    """Main"""
    path: str = "data/md"  # usr input

    words: list[str] = MdReader(path).get_md_names(raw=False)
    word_resonsse: dict[str, str] = {}
    for word in words:
        response: str = DICT_REQUESTER.parse_resonse(word)
        word_resonsse[word] = response

    writer = Writer(path)
    writer.write(word_resonsse)


if __name__ == "__main__":
    main()
