"""Main"""
import os
from typing import Optional

from merriam_api_parser.requset_resopnse import RequestResponse

DICT_KEY: Optional[str] = os.getenv("MERRIAM_WEBSTER_DICTONARY_KEY")
DICT_REQUESTER = RequestResponse(DICT_KEY)  # type: ignore


def main() -> None:
    """Main"""
    directory: str = "data/md"
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            filename.split(".")[0]
