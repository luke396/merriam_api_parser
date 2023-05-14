"""Format a string and return md-formatted text."""
import logging
import re


class TextTokenFormatter:
    """Format a string and return md-formatted text."""

    BASE_URL: str = "https://www.merriam-webster.com/dictionary/"
    BOLD_COLON_PATTERN: str = r"{bc}"
    WI_PATTERN: str = r"{wi}(\w+){/wi}"
    URL_PATTERNS: list[str] = [
        r"{(a_link)\|(\w+)}",
        r"{(sx)\|(\w*)\|(w*)\|}",
        r"{(d_link)\|(\w*)\|(\w*)}",
    ]

    def __init__(self) -> None:
        self.text: str = ""

    def parse_token(self, text: str) -> str:
        self.text = text
        self._parse_colon()
        self._parse_url()
        self._parse_wi()
        return self.text

    def _parse_colon(self) -> None:
        self._text_replace(self.BOLD_COLON_PATTERN, ": ")

    def _parse_wi(self) -> None:
        self._text_replace(self.WI_PATTERN, r"_\1_")

    def _parse_url(self) -> None:
        for pattern in self.URL_PATTERNS:
            try:
                matches = re.findall(pattern, self.text)
                for match in matches:
                    _tag, word = match[0], match[1]
                    md_format = f"[{word}]({self.BASE_URL}{word})"
                    self._text_replace(pattern, md_format)
            except re.error:
                logging.exception("Regex error Found")

    def _text_replace(self, pattern: str, replacement: str) -> None:
        self.text = re.sub(pattern, replacement, self.text)

    def __repr__(self) -> str:
        return f"TextTokenFormatter(text='{self.text}')"
