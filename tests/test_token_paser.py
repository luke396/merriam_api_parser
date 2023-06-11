import pytest

from merriam_api_parser._token_parser import TextTokenFormatter


def test_parse_token() -> None:
    formatter = TextTokenFormatter()
    _test_basic_text_formatting(formatter)
    _test_url_formatting(formatter)
    _test_multiple_urls(formatter)
    _test_invalid_input(formatter)
    _test_repr(formatter)


def _test_basic_text_formatting(formatter: TextTokenFormatter) -> None:
    assert formatter.parse_token("This is a test.") == "This is a test."
    assert (
        formatter.parse_token("This is {bc}bold not bold.")
        == "This is : bold not bold."
    )
    assert (
        formatter.parse_token("This is {wi}italicized{/wi} text.")
        == "This is _italicized_ text."
    )


def _test_url_formatting(formatter: TextTokenFormatter) -> None:
    assert (
        formatter.parse_token("{a_link|test word}")
        == "[test word](https://www.merriam-webster.com/dictionary/test-word)"
    )
    assert (
        formatter.parse_token("{sx||test word|}")
        == "[test word](https://www.merriam-webster.com/dictionary/test-word)"
    )
    assert (
        formatter.parse_token("{d_link|test|}")
        == "[test](https://www.merriam-webster.com/dictionary/test)"
    )


def _test_multiple_urls(formatter: TextTokenFormatter) -> None:
    assert formatter.parse_token(
        "{a_link|test word} and {sx||another-word|} are both words.",
    ) == (
        "[test word](https://www.merriam-webster.com/dictionary/test-word) "
        "and [another-word](https://www.merriam-webster.com/dictionary/another-word) "
        "are both words."
    )


def _test_invalid_input(formatter: TextTokenFormatter) -> None:
    with pytest.raises(TypeError):
        formatter.parse_token(None)  # type: ignore[arg-type]


def _test_repr(formatter: TextTokenFormatter) -> None:
    formatter.parse_token("This is a test.")
    assert repr(formatter) == "TextTokenFormatter(text='This is a test.')"
