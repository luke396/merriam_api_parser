from collections import defaultdict
from typing import Any

from merriam_api_parser._token_parser import TextTokenFormatter


class JsonParser:
    """Parse json data from Merriam-Webster Collegiate Dictionary API."""

    def __init__(self, json_data: dict[str, Any]) -> None:
        self.token_parser = TextTokenFormatter()
        self._data: dict[str, Any] = json_data
        self._meta: dict[str, Any] = self._data.get("meta", {})
        self._fl: str = self._data.get("fl", "")
        self._sense: dict[str, dict[str, Any]] = defaultdict(dict)
        self._md_text: str = ""
        self._parse_sseq()

    def _parse_sseq(self) -> None:
        """Parse the 'sseq' field of the JSON data."""
        sseq = self._data.get("def", [{}])[0].get("sseq", [])
        for single_sseq in sseq:
            self._parse_single_sseq(single_sseq)

    def _parse_single_sseq(self, single_sseq: list[Any]) -> None:
        """Parse a single 'sseq' element."""
        for single_sense in single_sseq:
            try:
                if single_sense[0] == "sense":
                    sense_number, definition_text = self._parse_single_sense(
                        single_sense,
                    )
                    self._sense[sense_number] = definition_text
                elif single_sense[0] == "pseq":
                    for single_sense_ in single_sense[1]:
                        sense_number, definition_text = self._parse_single_sense(
                            single_sense_,
                        )
                        self._sense[sense_number] = definition_text
            except (TypeError, KeyError, IndexError):
                continue

    def _parse_single_sense(
        self,
        single_sense: list[Any],
    ) -> tuple[str, dict[str, Any]]:
        """Parse a single 'sense' element."""
        single_sense_ele = defaultdict(str, single_sense[1])
        sense_number = single_sense_ele.get("sn", "")
        definition_text = self._parse_dt(single_sense_ele.get("dt", []))
        definition_text["text"] = self.token_parser.parse_token(definition_text["text"])
        definition_text["vis"] = [
            self.token_parser.parse_token(i["t"]) for i in definition_text["vis"]
        ]

        if single_sense_ele.get("sdsense") is not None:
            divided_sense = defaultdict(str, single_sense_ele["sdsense"])
            divided_sense_dt = self._parse_dt(divided_sense["dt"])
            definition_text["sdsense_sd"] = divided_sense["sd"]
            definition_text["sdsense_text"] = self.token_parser.parse_token(
                divided_sense_dt["text"],
            )

        return sense_number, definition_text

    def _parse_dt(self, origin_dt: list[list[str | Any]]) -> dict[str, Any]:
        """Parse a 'dt' element."""
        dt_ele = self._name_ele_constructor(origin_dt)
        return {"text": dt_ele.get("text", ""), "vis": dt_ele.get("vis", "")}

    # not change to stasticmethod
    def _name_ele_constructor(self, lst: list[list[str | Any]]) -> dict[str, Any]:
        """Construct a dictionary from a list of lists."""
        names = []
        ele = []
        for single in lst:
            names.append(single[0])
            ele.append(single[1])
        return dict(zip(names, ele, strict=True))

    def get_md_text(self) -> str:
        """Get the markdown text."""
        # note's metadata
        self._add_three_hyphen_up()
        self._add_synonym()
        self._add_three_hyphen_down()

        self._add_head(self._meta.get("id", ""), 1)
        self._add_all_sense()
        return self._md_text

    def _add_all_sense(self) -> None:
        """Add all senses to the markdown text."""
        for head, sense in self._sense.items():
            self._add_head(head, level=2)
            self._add_sense(sense, "text", "vis")
            if sense.get("sdsense_sd") is not None:
                self._add_head(sense.get("sdsense_sd", ""), level=3)
                self._add_sense(sense, "sdsense_text", "sdense_vis")

    def _add_sense(
        self,
        sense: dict[str, str],
        sense_text: str,
        illustration: str,
    ) -> None:
        """Add a sense to the markdown text."""
        self._add_md_new_line()
        self._md_text += _md_text_color(f"{sense.get(sense_text, '')}")
        self._add_md_new_line()
        self._md_text += "\n\n".join(sense.get(illustration, ""))

    def _add_head(self, head: str, level: int) -> None:
        """Add a heading to the markdown text."""
        self._add_md_new_line()
        self._md_text += f"{'#' * level} {head}"

    def _add_md_new_line(self) -> None:
        """Add a new line to the markdown text."""
        self._md_text += "\n\n"

    def _add_three_hyphen_up(
        self,
    ) -> None:
        """Add three hyphens to the note's metadata."""
        self._md_text += "---\n"

    def _add_three_hyphen_down(
        self,
    ) -> None:
        self._md_text += "---"

    def _add_synonym(self) -> None:
        """Add synonyms to the note's metadata."""
        if synonym := self._meta.get("stems", []):
            self._md_text += f"aliases: {', '.join(synonym)}\n"


def _md_text_color(text: str, color: str = "#FFB8EBA6") -> str:
    """Add color to text in the markdown format."""
    return f'<mark style="background: {color};">{text}</mark>' if text else ""
