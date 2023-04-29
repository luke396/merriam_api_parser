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
        self._parse_wi()
        # print(self.text)
        return self.text

    def _parse_bold_colon(self) -> None:
        """Convert '{bc}' to md-format ': '."""
        self._text_replace_2(r"{bc}", ": ")

    def _parse_wi(self) -> None:
        """Convert '{wi}word{/wi}' to md-format '_word_'."""
        self._text_replace_2(r"{wi}(\w+){/wi}", r"_\1_")

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

    def _text_replace_2(self, arg0, arg1) -> None:
        pattern: str = arg0
        replacement: str = arg1
        self.text = re.sub(pattern, replacement, self.text)
