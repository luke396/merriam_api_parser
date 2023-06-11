from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from merriam_api_parser._io import Reader, Writer


@pytest.fixture()
def temp_dir() -> TemporaryDirectory[str]:
    with TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture()
def temp_file(temp_dir: TemporaryDirectory[str]) -> Path:
    file_path = temp_dir / "test.md"
    file_path.write_text("# Test\n\nThis is a test.", encoding="UTF-8")
    return file_path


def test_reader_single_file(temp_file: TemporaryDirectory) -> None:
    reader = Reader(temp_file)
    assert reader.get_md_names() == ["test"]


def test_reader_directory(temp_dir: TemporaryDirectory) -> None:
    file_path = temp_dir / "test.md"
    file_path.write_text("# Test\n\nThis is a test.", encoding="UTF-8")
    reader = Reader(Path(temp_dir))
    assert reader.get_md_names() == ["test"]


def test_reader_directory_no_md_files(temp_dir: TemporaryDirectory) -> None:
    file_path = Path(temp_dir) / "test.txt"
    file_path.write_text("This is a test.", encoding="UTF-8")
    reader = Reader(temp_dir)
    assert reader.get_md_names() == []


def test_writer(temp_dir: TemporaryDirectory) -> None:
    file_path = temp_dir / "test.md"
    writer = Writer(file_path)
    writer.write("# Test\n\nThis is a test.")
    assert file_path.read_text(encoding="UTF-8") == "# Test\n\nThis is a test."
