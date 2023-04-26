"""Parse the json file and return needed data."""
import json
from collections import defaultdict
from typing import Any

from merriam_api_parser._text_formatter import TextTokenFormatter

# TODO: may be create a NewType for json data


class JsonParser:
    """Parse a json file and return needed data."""

    def __init__(self, json_data: dict[str, Any]) -> None:
        """Init the class."""
        self.token_parser = TextTokenFormatter()
        self._data: dict[str, Any] = json_data

        self._def: dict[str, Any] = self._data["def"][0]  # definition section
        self._sseq: list[Any] = self._def.get("sseq", None)  # sense sequence
        self._vb: str = self._def.get("vb", None)  # verb divider
        self._sense: defaultdict[
            str, defaultdict[str, Any]
        ] = defaultdict()  # sense with number as key

        self._md_text: str = ""
        self._parse_sseq()

    def _parse_sseq(self) -> None:
        """Parse the sseq section of the json file."""
        for sense in self._sseq:
            self._parse_single_sseq(sense)

    def _parse_single_sseq(self, sense) -> None:
        """Parse a single sense in sseq section."""
        single_sense: list[str | dict[str, Any]]
        for single_sense in sense:
            single_ele: defaultdict[str, Any] = self._parse_single_sense(single_sense)

            sense_number: str = single_ele["sn"]  # sense number

            # definition text
            definition_text: defaultdict[str, Any] = self._parse_dt(single_ele["dt"])
            definition_text["text"] = self.token_parser.parse_token(
                definition_text["text"]
            )

            self._sense[sense_number] = definition_text

            # TODO continue here parse more inside single sense

    def _parse_single_sense(
        self, single_sense: list[str | dict[str, Any]]
    ) -> defaultdict[str, Any]:
        assert len(single_sense) == 2  # noqa: PLR2004
        assert single_sense[0] == "sense"
        single_sense_element: dict[str, Any] = single_sense[1]  # type: ignore
        return defaultdict(
            str,
            zip(
                single_sense_element.keys(), single_sense_element.values(), strict=True
            ),
        )

    def _parse_dt(self, origin_dt: list[list[str | Any]]) -> defaultdict[str, Any]:
        dt_ele: defaultdict[str, Any] = self._name_ele_constructor(origin_dt)
        name: list[str] = ["text", "vis"]
        return defaultdict(str, zip(name, [dt_ele[i] for i in name], strict=True))

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
        return defaultdict(str, zip(names, ele, strict=True))

    def md_text(self) -> str:
        """Return the md text."""
        print(self._sense)
        # TODO: to format and return all md text (eg: head, new lines, etc.)
        return self._md_text


def main() -> None:
    """main for testing."""
    file_name = "data/json/voluminous.json"
    with open(file_name, "r", encoding="UTF-8") as file:
        data = json.loads(file.read())
        JsonParser(data)


if __name__ == "__main__":
    main()
