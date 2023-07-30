"""Utility functions."""
import asyncio
import json
import logging
import os
from pathlib import Path
from typing import Any

import requests

from merriam_api_parser._io import MdFormatter, Reader, Writer
from merriam_api_parser._json_parser import JsonParser


class MerriamWebsterAPI:
    """Request and parse response from Merriam-Webster Collegiate Dictionary API."""

    API_URL: str = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/"

    def __init__(self, api_key: str) -> None:
        self.api_key: str = api_key

    def parse_response(self, word: str) -> str:
        """Parse response to md-formatted text."""
        url: str = f"{self.API_URL}/{word}?key={self.api_key}"
        try:
            response: requests.Response = requests.get(url, timeout=3000)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            response = requests.get(url, timeout=3000)
        except requests.exceptions.RequestException:
            logging.exception("Failed to get response for %s:", word)
            return ""

        json_res: list[dict[str, Any]] = json.loads(response.text)
        return JsonParser(
            json_res[0],
        ).get_md_text()  # TODO: json_res[0] maybe more specific

    async def process_word(self, word: str) -> tuple[str, str]:
        """Process a single word and return the response."""
        try:
            logging.info("Getting response for %s", word)
            response = await asyncio.to_thread(self.parse_response, word)
            logging.info("Got response for %s", word)
        except Exception as error:
            msg: str = f"Failed to get response for {word}: {error}"
            logging.exception(msg)
            response = ""
        return word, response


def init_api() -> MerriamWebsterAPI:
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


async def main() -> None:
    """Run."""
    configure_logging()
    request_response: MerriamWebsterAPI = init_api()
    user_input = process_user_input(get_user_input())

    if isinstance(user_input, Path):  # TODO: increase coverage
        path = user_input
        tasks = [
            request_response.process_word(word) for word in Reader(path).get_md_names()
        ]
        for word, response in await asyncio.gather(*tasks):
            Writer(path / f"{word}.md").write(response)

    elif isinstance(user_input, str):
        path = Path("data/md/")
        word, response = await request_response.process_word(user_input)
        Writer(path / f"{word}.md").write(response)

    else:
        msg = "Invalid user input"
        raise TypeError(msg)

    MdFormatter(path).md_format()


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
