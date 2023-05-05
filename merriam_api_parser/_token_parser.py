"""Format a string and return md-formatted text."""
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
        return self.text

    def _parse_bold_colon(self) -> None:
        """Convert '{bc}' to md-format ': '."""
        self._text_replace(r"{bc}", ": ")

    def _parse_wi(self) -> None:
        """Convert '{wi}word{/wi}' to md-format '_word_'."""
        self._text_replace(r"{wi}(\w+){/wi}", r"_\1_")

    def _parser_url(self) -> None:
        r"""
        Convert url_token to md-format '\[word\](url)'.

        Included:
        "{a_link|word}", "{sx|word_1|word_2|}", "{d_link|word_1|word_2}"
        """
        self._convert_url(r"{(a_link)\|(\w+)}")
        self._convert_url(r"{(sx)\|(\w*)\|(w*)\|}")
        self._convert_url(r"{(d_link)\|(\w*)\|(\w*)}")

    def _convert_url(self, pattern: str) -> None:
        r"""Convert url to md-format \[word\](url)."""
        matches: list[str] = re.findall(pattern, self.text)
        for match in matches:
            _tag: str = match[0]
            word: str = match[1] or match[2]
            md_format: str = f"[{word}]({self.base_url}{word})"
            self._text_replace(pattern, md_format)

    def _text_replace(self, pattern: str, replacement: str) -> None:
        self.text = re.sub(pattern, replacement, self.text)
