"""Request and parse response from Merriam-Webster Collegiate Dictionary API."""

import json
from typing import Any

import requests

from merriam_api_parser.core._json_parser import JsonParser


class MerriamWebsterAPI:
    """Request and parse response from Merriam-Webster Collegiate Dictionary API."""

    API_URL: str = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/"

    def __init__(self, api_key: str) -> None:
        self.api_key: str = api_key

    def parse_response(self, word: str) -> str:
        """Parse response to md-formatted text."""
        url: str = f"{self.API_URL}/{word}?key={self.api_key}"
        try:
            response: requests.Response = requests.get(url, timeout=5)
            json_res: list[dict[str, Any]] = json.loads(response.text)
            return JsonParser(
                json_res[0],
            ).get_md_text()  # TODO: json_res[0] maybe more specific
        except Exception:  # noqa: BLE001
            return ""
