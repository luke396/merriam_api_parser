import pytest

from merriam_api_parser import utility


@pytest.mark.asyncio()
async def test_main_with_single_word(mocker):
    mocker.patch("merriam_api_parser.utility.get_user_input", return_value="word")
    mocker.patch("merriam_api_parser.utility.process_user_input", return_value="word")
    mock_process_word = mocker.patch(
        "merriam_api_parser.utility.MerriamWebsterAPI.process_word",
    )
    mock_process_word.return_value = ("word", "response")
    mock_write = mocker.patch("merriam_api_parser._io.Writer.write")

    await utility.main()

    mock_process_word.assert_called_once_with("word")
    mock_write.assert_called_once_with("response")


def test_configure_logging(mocker):
    mock_basic_config = mocker.patch("logging.basicConfig")
    mock_file_handler = mocker.patch("logging.FileHandler")
    mock_stream_handler = mocker.patch("logging.StreamHandler")

    utility.configure_logging()

    mock_basic_config.assert_called_once_with(
        level=mocker.ANY,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[mock_file_handler(), mock_stream_handler()],
    )
