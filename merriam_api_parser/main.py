import os
from typing import Optional

from merriam_api_parser.requset_resopnse import RequestResponse

dict_key: Optional[str] = os.getenv("MERRIAM_WEBSTER_DICTONARY_KEY")
requester = RequestResponse(dict_key)  # type: ignore
directory: str = "data/md"
for filename in os.listdir(directory):
    if filename.endswith(".md"):
        word = filename.split(".")[0]
