"""Main, please set environment variable "MERRIAM_WEBSTER_DICTIONARY_KEY" first"""
import os
from typing import Optional

from merriam_api_parser._io import Reader, Writer
from merriam_api_parser._requset_resopnse import RequestResponse

DICT_KEY: Optional[str] = os.getenv("MERRIAM_WEBSTER_DICTIONARY_KEY")
DICT_REQUESTER = RequestResponse(DICT_KEY)  # type: ignore


def get_words(path: str) -> list[str]:
    """Get words from file"""
    reader = Reader(path)
    return reader.get_md_names(raw=False)


def main() -> None:
    """Main"""
    path: str = input("Please input path, default is data/md/:\n") or "data/md/"
    path = path if path.endswith("/") else f"{path}/"

    words: list[str] = get_words(path)
    word_responses: dict[str, str] = {}
    for word in words:
        response: str = DICT_REQUESTER.parse_resonse(word)
        word_responses[word] = response

    writer = Writer(path)
    writer.write(word_responses)

    md_foramt: str = f"markdownlint {path}*.md -f"
    print(f"\nFormat md response files with: {md_foramt}")
    os.system(md_foramt)


if __name__ == "__main__":
    main()
