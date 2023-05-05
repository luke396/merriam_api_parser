"""Request and parse response from Merriam-Webster Collegiate Dictionary API."""

import json
from typing import Any

import requests

from merriam_api_parser._json_parser import JsonParser


class RequestResponse:
    """Requset and parse response from Merriam-Webster Collegiate Dictionary API."""

    def __init__(self, api_key: str) -> None:
        self.api_key: str = api_key

    def parse_resonse(self, word: str) -> str:
        """Parse response to md-formated text."""
        url: str = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={self.api_key}"  # noqa: E501
        response: requests.Response = requests.get(url, timeout=5)
        json_res: list[dict[str, Any]] = json.loads(response.text)
        # there should return all text write to md file
        return JsonParser(json_res[0]).get_md_text()
        # TODO: json_res[0] may be wrong
