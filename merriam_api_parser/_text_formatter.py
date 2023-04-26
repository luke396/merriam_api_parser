"""Format a string and return md-formatted text.
"""
import re


class TextTokenFormatter:
    """Format a token from text and return needed data."""

    def __init__(self) -> None:
        self.base_url: str = "https://www.merriam-webster.com/dictionary/"
        self.text: str = ""

    def parse_token(self, text: str) -> str:
        """Parse tokens from text and return needed data."""
        self.text = text
        self._parse_bold_colon()
        self._parser_url()
        # print(self.text)
        return self.text

    def _parse_bold_colon(self) -> None:
        """Convert '{bc}' to md-format ': '."""
        pattern: str = r"{bc}"
        replacement: str = ": "
        self.text = re.sub(pattern, replacement, self.text)

    def _parser_url(self) -> None:
        """Convert '{a_link|word}' or '{sx|word||}' to md-format '\\[word](url)'."""
        self._convert_url(r"{(a_link)\|(\w+)}")
        self._convert_url(r"{(sx)\|(\w+)\|\|}")

    def _convert_url(self, pattern: str) -> None:
        """Convert url to md-format '\\[word](url)'."""
        matches: list[str] = re.findall(pattern, self.text)
        for match in matches:
            tag: str = match[0]
            word: str = match[1]
            md_format: str = f"[{word}]({self.base_url}{word})"
            self._text_replace(tag, word, md_format)

    def _text_replace(self, tag: str, word: str, md_format: str) -> None:
        if tag == "a_link":
            self.text = self.text.replace(f"{{{tag}|{word}}}", md_format)
        elif tag == "sx":
            self.text = self.text.replace(f"{{{tag}|{word}||}}", md_format)
        elif tag == "bc":
            self.text = self.text.replace(f"{{{tag}}}{word}", md_format)
