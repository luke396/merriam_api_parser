"""Parse the json file and return needed data."""
import json
from collections import defaultdict
from typing import Any

from merriam_api.formatter import TextTokenFormatter

# TODO: may be create a NewType for json data


class JsonParser:
    """Parse a json file and return needed data."""

    def __init__(self, json_file: str) -> None:
        self.token_parser = TextTokenFormatter()

        with open(json_file, "r", encoding="UTF-8") as data:
            self._data: dict[str, Any] = json.load(data)
        self._def: dict[str, Any] = self._data["def"][0]  # definition section
        self._sseq: list[Any] = self._def.get("sseq", None)  # sense sequence
        self._vb: str = self._def.get("vb", None)  # verb divider
        self.sense: defaultdict[
            str, defaultdict[str, Any]
        ] = defaultdict()  # sense with number as key
        self._parse_sseq()

    def _parse_sseq(self) -> None:
        for sense in self._sseq:
            single_sense: list[str | dict[str, str | Any]]
            for single_sense in sense:
                single_ele: defaultdict[str, Any] = self._parse_single_sense(
                    single_sense
                )
                sense_number: str = single_ele["sn"]  # sense number
                definition_text: defaultdict[str, Any] = self._parse_dt(
                    single_ele["dt"]
                )  # definition text
                self.sense[sense_number] = definition_text
                self.token_parser.parse_token(definition_text["text"])

    def _parse_single_sense(
        self, single_sense: list[str | dict[str, Any]]
    ) -> defaultdict[str, Any]:
        assert len(single_sense) == 2
        assert single_sense[0] == "sense"
        single_sense_element: dict[str, str | Any] = single_sense[1]  # type: ignore
        return defaultdict(
            str, zip(single_sense_element.keys(), single_sense_element.values())
        )

    def _parse_dt(self, origin_dt: list[list[str | Any]]) -> defaultdict[str, Any]:
        dt_ele: defaultdict[str, Any] = self._name_ele_constructor(origin_dt)
        name = ["text", "vis"]
        return defaultdict(str, zip(name, [dt_ele[i] for i in name]))

    def _name_ele_constructor(
        self, lst: list[list[str | Any]]
    ) -> defaultdict[str, Any]:
        """Convert a list of list to a dict with the first element as key.

        Example:
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
            assert isinstance(single[0], str)
            names.append(single[0])
            ele.append(single[1])
        return defaultdict(str, zip(names, ele))


FILE = "src/voluminous.json"
if __name__ == "__main__":
    case = JsonParser(FILE)
