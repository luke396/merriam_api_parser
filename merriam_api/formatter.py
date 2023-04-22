"""Format a string using a dictionary of values.
"""
import re


class TextTokenFormatter:
    """Format a token from text and return needed data.
    """

    def __init__(self) -> None:
        self.base_url = "https://www.merriam-webster.com/dictionary/"

    def parse_token(self, text: str) -> None:
        self._parse_url(text)

    def _parse_url(self, text: str):
        """Convert {a_link|word} to md-format-url.
        """
        pattern = r"{(a_link)\|(\w+)}"
        matches: list[str] = re.findall(pattern, text)
        for match in matches:
            tag, word = match
            md_url = f"[{word}]({self.base_url}{word})"
            text = text.replace(f"{{{tag}|{word}}}", md_url)
        return text
