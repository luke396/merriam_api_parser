"""Format a string and return md-formatted text."""
import re


class TextTokenFormatter:
    """Format a string and return md-formatted text."""

    BASE_URL: str = "https://www.merriam-webster.com/dictionary/"
    BOLD_COLON_PATTERN: str = r"{bc}"
    WI_PATTERN: str = r"{wi}(\w+){/wi}"
    WORD_PATTERN: str = r"(\w*\-*\ *\w*)"
    URL_PATTERNS: list[str] = [
        r"{(a_link)\|" + WORD_PATTERN + r"}",
        r"{(sx)\|" + WORD_PATTERN + r"\|" + WORD_PATTERN + r"\|}",
        r"{(d_link)\|" + WORD_PATTERN + r"\|" + WORD_PATTERN + r"}",
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
        self.text = re.sub(self.BOLD_COLON_PATTERN, ": ", self.text)

    def _parse_wi(self) -> None:
        self.text = re.sub(self.WI_PATTERN, r"_\1_", self.text)

    def _parse_url(self) -> None:
        for pattern in self.URL_PATTERNS:
            matches = re.findall(pattern, self.text)
            for match in matches:
                _tag, word = match[0], match[1] or match[2]
                md_format = f"[{word}]({self.BASE_URL}{word.replace(' ', '-')})"
                self.text = re.sub(pattern, md_format, self.text)

    def __repr__(self) -> str:
        return f"TextTokenFormatter(text='{self.text}')"
