"""Request and parse response from Merriam-Webster Collegiate Dictionary API"""

import requests


class RequestResponse:
    """Requset and parse response from Merriam-Webster Collegiate Dictionary API"""

    def __init__(self, api_key: str) -> None:
        self.api_key: str = api_key
        self.md_response: str = ""

    def parse_resonse(self, word: str) -> str:
        """Parse response to md-formated text"""
        url: str = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={self.api_key}"  # pylint: disable=line-too-long  # noqa: E501
        response: requests.Response = requests.get(url, timeout=5)
        self.md_response = response.text
        return self.md_response
