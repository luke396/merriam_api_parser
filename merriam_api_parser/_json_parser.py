"""Parse the json file and return needed data."""
from collections import defaultdict
from typing import Any

from merriam_api_parser._token_parser import TextTokenFormatter

# TODO: may be create a NewType for json data


class JsonParser:
    """Parse a json file and return needed data."""

    def __init__(self, json_data: dict[str, Any]) -> None:
        """Init the class."""
        self.token_parser = TextTokenFormatter()
        self._data = json_data
        self._meta = self._data["meta"]
        self._fl = self._data["fl"]
        self._sense: defaultdict[str, defaultdict[str, Any]] = defaultdict()

        self._md_text = ""

        self._parse_sseq()

    def _parse_sseq(self) -> None:
        sseq: list[Any] = self._data["def"][0].get("sseq", None)  # sense sequence
        for single_sseq in sseq:
            self._parse_single_sseq(single_sseq)

    def _parse_single_sseq(self, single_sseq: list[Any]) -> None:
        for single_sense in single_sseq:
            if single_sense[0] == "sense":
                sense_number, definition_text = self._parse_single_sense(single_sense)
                self._sense[sense_number] = definition_text
            elif single_sense[0] == "pseq":  # has nested sense
                # TODO: head level should lower than sense
                for single_sense_ in single_sense[1]:
                    sense_number, definition_text = self._parse_single_sense(
                        single_sense_,
                    )
                    self._sense[sense_number] = definition_text

    def _parse_single_sense(
        self,
        single_sense: list[Any],
    ) -> tuple[str, defaultdict[str, Any]]:
        single_sense_ele = _convert_dict_to_defaultdict(single_sense[1])
        sense_number = single_sense_ele["sn"]
        definition_text = self._parse_dt(single_sense_ele["dt"])
        definition_text["text"] = self.token_parser.parse_token(definition_text["text"])
        definition_text["vis"] = [
            self.token_parser.parse_token(i["t"]) for i in definition_text["vis"]
        ]

        if single_sense_ele.get("sdsense") is not None:
            divided_sense = _convert_dict_to_defaultdict(single_sense_ele["sdsense"])
            divided_sense_dt = self._parse_dt(divided_sense["dt"])
            definition_text["sdense_sd"] = divided_sense["sd"]
            definition_text["sdense_text"] = self.token_parser.parse_token(
                divided_sense_dt["text"],
            )
            definition_text["sdense_vis"] = [
                self.token_parser.parse_token(i["t"]) for i in divided_sense["vis"]
            ]

        return sense_number, definition_text

    def _parse_dt(self, origin_dt: list[list[str | Any]]) -> defaultdict[str, Any]:
        dt_ele = self._name_ele_constructor(origin_dt)
        name = ["text", "vis"]
        return defaultdict(str, zip(name, [dt_ele[i] for i in name], strict=True))

    def _name_ele_constructor(
        self,
        lst: list[list[str | Any]],
    ) -> defaultdict[str, Any]:
        names = []
        ele = []
        for single in lst:
            names.append(single[0])
            ele.append(single[1])
        return defaultdict(str, zip(names, ele, strict=True))

    def _sense_to_md(self) -> None:
        for head, sense in self._sense.items():
            self._add_head(head, 2)
            self._add_sense(sense, "text", "vis")
            self._add_head(sense["sdense_sd"], level=3)
            self._add_sense(sense, "sdense_text", "sdense_vis")

    def _add_sense(
        self,
        sense: defaultdict[str, str],
        sense_text: str,
        illustration: str,
    ) -> None:
        self._add_md_new_line()
        self._md_text += _md_text_color(f"{sense[sense_text]}")
        self._add_md_new_line()
        self._md_text += "\n\n".join(sense[illustration])
        self._add_md_new_line()

    def _add_head(self, key: str, level: int) -> None:
        if key:
            pre = "#" * level
            self._md_text += f"{pre} {key}\n"

    def _add_md_new_line(self) -> None:
        self._md_text += "\n\n"

    def get_md_text(self) -> str:
        self._add_head(self._meta["id"], 1)
        self._sense_to_md()
        return self._md_text


def _md_text_color(text: str, color: str = "#FFB8EBA6") -> str:
    return f'<mark style="background: {color};">{text}</mark>' if text else ""


def _convert_dict_to_defaultdict(_dict: dict[Any, Any]) -> defaultdict[Any, Any]:
    return defaultdict(str, zip(_dict.keys(), _dict.values(), strict=True))
