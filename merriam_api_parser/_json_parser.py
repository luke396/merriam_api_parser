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
        self._data: dict[str, Any] = json_data

        # TODO: maybe not needed set self
        # meta section
        self._meta: dict[str, Any] = self._data["meta"]
        # functional label
        self._fl: str = self._data["fl"]

        # sense with number as key
        self._sense: defaultdict[str, defaultdict[str, Any]] = defaultdict()

        self._md_text: str = ""
        self._parse_sseq()

    def _parse_sseq(self) -> None:
        """Parse the sseq section of the json file.

        sseq section is a list of list of single_sseq,\
            each single_sseq contains sense and example.
        """
        sseq: list[Any] = self._data["def"][0].get("sseq", None)  # sense sequence
        for single_sseq in sseq:
            self._parse_single_sseq(single_sseq)

    def _parse_single_sseq(self, single_sseq: list[Any]) -> None:
        """Parse single sense which contains sense and example, is what we need."""
        single_sense: list[Any]
        for single_sense in single_sseq:
            single_sense_ele: defaultdict[str, Any] = _convert_dict_to_defaultdict(
                single_sense[1],
            )

            sense_number: str = single_sense_ele["sn"]

            definition_text: defaultdict[str, Any] = self._parse_dt(
                single_sense_ele["dt"],
            )
            definition_text["text"] = self.token_parser.parse_token(
                definition_text["text"],
            )
            definition_text["vis"] = [
                self.token_parser.parse_token(i["t"]) for i in definition_text["vis"]
            ]  # ignore `author` tag within example, for now

            if single_sense_ele.get("sdsense", None) is not None:
                divided_sense: dict[str, Any] = _convert_dict_to_defaultdict(
                    single_sense_ele["sdsense"],
                )
                divided_sense_dt: defaultdict[str, Any] = self._parse_dt(
                    divided_sense["dt"],
                )
                definition_text["sdense_sd"] = divided_sense["sd"]
                definition_text["sdense_text"] = self.token_parser.parse_token(
                    divided_sense_dt["text"],
                )
                definition_text["sdense_vis"] = [
                    self.token_parser.parse_token(i["t"]) for i in divided_sense["vis"]
                ]

            self._sense[sense_number] = definition_text

            # TODO: continue here parse more inside single sense

    def _parse_dt(self, origin_dt: list[list[str | Any]]) -> defaultdict[str, Any]:
        """Return 'text' and 'vis' inside dt section."""
        dt_ele: defaultdict[str, Any] = self._name_ele_constructor(origin_dt)
        name: list[str] = ["text", "vis"]  # could be more
        return defaultdict(str, zip(name, [dt_ele[i] for i in name], strict=True))

    def _name_ele_constructor(
        self,
        lst: list[list[str | Any]],
    ) -> defaultdict[str, Any]:
        """Convert a list of list to a dict with the first element as key.

        Example:
        -------
            >>> _name_ele([
                "text",
                "{bc}having or marked by /
                great {a_link|volume} or bulk {bc}{sx|large||} "
            ],
            [
                "vis",
                [
                {
                    "t": "long {wi}voluminous{/wi} tresses"
                }
                ]
            ]
            ])

            >>> {
                'text': '{bc}having or marked by great {a_link|volume}/
                            or bulk {bc}{sx|large||} ',
                'vis': [{'t': 'long {wi}voluminous{/wi} tresses'}]}
        """
        names: list[str] = []
        ele: list[Any] = []
        for single in lst:
            names.append(single[0])
            ele.append(single[1])
        return defaultdict(str, zip(names, ele, strict=True))

    def _sense_to_md(self) -> None:
        """Convert the sense to md text."""
        for head, sense in self._sense.items():
            self._add_head(head, 2)
            self._add_sense(sense, "text", "vis")
            self._add_head(sense["sdense_sd"], level=3)
            self._add_sense(sense, "sdense_text", "sdense_vis")

    def _add_sense(
        self,
        sense: dict[str, str],
        sense_text: str,
        illustration: str,
    ) -> None:
        """Add sense to md text.

        Args:
            sense (dict[str, str]): Sense dict.
            sense_text (str): Sense text, will be colored.
            illustration (str): Illustration text.
        """
        self._add_md_new_line()

        self._md_text += _md_text_color(f"{sense[sense_text]}")
        self._add_md_new_line()

        self._md_text += "\n\n".join(sense[illustration])
        self._add_md_new_line()

    def _add_head(self, key: str, level: int) -> None:
        if key:
            pre: str = "#" * level
            self._md_text += f"{pre} {key}\n"

    def _add_md_new_line(self) -> None:
        self._md_text += "\n\n"

    def get_md_text(self) -> str:
        """Return the md text."""
        self._add_head(self._meta["id"], 1)  # header
        self._sense_to_md()
        # TODO: to format and return all md text (eg: head, new lines, etc.)
        return self._md_text


def _md_text_color(text: str, color: str = "#FFB8EBA6") -> str:
    """Return the text with color."""
    return f'<mark style="background: {color};">{text}</mark>' if text else ""


def _convert_dict_to_defaultdict(_dict: dict[Any, Any]) -> defaultdict[Any, Any]:
    return defaultdict(str, zip(_dict.keys(), _dict.values(), strict=True))
