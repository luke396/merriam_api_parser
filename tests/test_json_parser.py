import json
from pathlib import Path
from typing import Any

import pytest

from merriam_api_parser._json_parser import JsonParser


@pytest.fixture()
def json_data() -> dict[str, Any]:
    with Path("tests/test_data.json").open(encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture()
def single_sense() -> list[Any]:
    return [
        "sense",
        {
            "sn": "1",
            "dt": [
                ["text", "test definition"],
                [
                    "vis",
                    [{"t": "test illustration"}],
                ],
            ],
            "sdsense": {"sd": "sense divider", "dt": [["text", "test definition"]]},
        },
    ]


@pytest.fixture()
def single_sseq() -> list[Any]:
    return [
        [
            "sense",
            {
                "sn": "1",
                "dt": [
                    ["text", "test definition"],
                    [
                        "vis",
                        [{"t": "test illustration"}],
                    ],
                ],
                "sdsense": {"sd": "sense divider", "dt": [["text", "test definition"]]},
            },
        ],
        [
            "pseq",
            [
                [
                    "sense",
                    {
                        "sn": "1 a",
                        "dt": [
                            ["text", "test definition"],
                            [
                                "vis",
                                [{"t": "test illustration"}],
                            ],
                        ],
                    },
                ],
            ],
        ],
    ]


@pytest.fixture()
def single_pseq() -> list[Any]:
    return [
        "pseq",
        [
            [
                "sense",
                {
                    "sn": "1 a",
                    "dt": [
                        ["text", "test definition"],
                        [
                            "vis",
                            [{"t": "test illustration"}],
                        ],
                    ],
                },
            ],
        ],
    ]


@pytest.fixture()
def empty_parser() -> JsonParser:
    return JsonParser({})


@pytest.fixture()
def full_parser(json_data) -> JsonParser:
    return JsonParser(json_data)


def test_single_sseq(json_data, single_sseq):
    _single_sseq = json_data["def"][0]["sseq"][0]
    assert _single_sseq == single_sseq


def test_single_sense(json_data, single_sense):
    _single_sense = json_data["def"][0]["sseq"][0][0]
    assert _single_sense == single_sense


def test_parse_sseq(full_parser):
    parser = full_parser
    parser._parse_sseq()
    assert parser._sense == {
        "1": {
            "text": "test definition",
            "vis": ["test illustration"],
            "sdsense_sd": "sense divider",
            "sdsense_text": "test definition",
        },
        "1 a": {"text": "test definition", "vis": ["test illustration"]},
    }


def test_parse_sseq_empty(empty_parser):
    parser = empty_parser
    parser._parse_sseq()
    assert parser._sense == {}


def test_parse_single_sseq(full_parser, single_sseq):
    parser = full_parser
    parser._parse_single_sseq(single_sseq)
    assert parser._sense == {
        "1": {
            "text": "test definition",
            "vis": ["test illustration"],
            "sdsense_sd": "sense divider",
            "sdsense_text": "test definition",
        },
        "1 a": {"text": "test definition", "vis": ["test illustration"]},
    }


def test_pase_single_sseq_pseq(full_parser, single_pseq):
    parser = full_parser
    parser._parse_single_sseq(single_pseq)
    assert parser._sense == {
        "1": {
            "text": "test definition",
            "vis": ["test illustration"],
            "sdsense_sd": "sense divider",
            "sdsense_text": "test definition",
        },
        "1 a": {"text": "test definition", "vis": ["test illustration"]},
    }


def test_parse_single_sseq_index_error(empty_parser):
    # For coverage
    parser = empty_parser
    parser._parse_single_sseq([{"test": "test"}])


def test_parse_single_sense(empty_parser, single_sense):
    parser = empty_parser
    sense_number, definition_text = parser._parse_single_sense(single_sense)
    assert sense_number == "1"
    assert definition_text == {
        "text": "test definition",
        "vis": ["test illustration"],
        "sdsense_sd": "sense divider",
        "sdsense_text": "test definition",
    }


def test_parse_dt(empty_parser):
    parser = empty_parser
    origin_dt = [["text", "test definition"]]
    dt = parser._parse_dt(origin_dt)
    assert dt == {"text": "test definition", "vis": ""}


def test_name_ele_constructor(empty_parser):
    parser = empty_parser
    lst = [["text", "test definition"]]
    name_ele = parser._name_ele_constructor(lst)
    assert name_ele == {"text": "test definition"}


def test_add_head(empty_parser):
    parser = empty_parser
    parser._add_head("test", 1)
    assert parser._md_text == "\n\n# test"


def test_add_sense(empty_parser):
    parser = empty_parser
    sense = {"text": "test definition", "vis": ["test illustration"]}
    parser._add_sense(sense, "text", "vis")
    assert parser._md_text == (
        '\n\n<mark style="background: #FFB8EBA6;">test definition</mark>\n\ntest illustration'
    )


def test_add_md_new_line(empty_parser):
    parser = empty_parser
    parser._add_md_new_line()
    assert parser._md_text == "\n\n"


def test_add_three_hyphen(empty_parser):
    parser = empty_parser
    parser._add_three_hyphen_up()
    parser._add_three_hyphen_down()
    assert parser._md_text == "---\n---"


def test_add_synonym(full_parser):
    parser = full_parser
    parser._add_synonym()
    assert parser._md_text == "aliases: test_alias\n"


def test_add_all_sense(full_parser):
    parser = full_parser
    parser._add_all_sense()
    assert parser._md_text == (
        "\n\n## 1\n\n"
        '<mark style="background: #FFB8EBA6;">test definition</mark>\n\n'
        "test illustration\n\n"
        "### sense divider\n\n"
        '<mark style="background: #FFB8EBA6;">test definition</mark>\n\n'
        "\n\n"
        "## 1 a\n\n"
        '<mark style="background: #FFB8EBA6;">test definition</mark>\n\n'
        "test illustration"
    )


# Note that formatter will add new last line
def test_get_md_text(full_parser):
    parser = full_parser
    with Path("tests/test_data.md").open(encoding="utf-8") as f:
        md = f.read()
    assert parser.get_md_text() == md


# TODO: more tests to 100% coverage
# TODO: add 100% coverage requirement to pre-commit
