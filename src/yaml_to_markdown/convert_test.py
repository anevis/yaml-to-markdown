from io import StringIO
from pathlib import Path
from unittest.mock import Mock, mock_open, patch

import pytest
from click.testing import CliRunner

from yaml_to_markdown.convert import convert, main

_JSON_DATA = '{"key": "value"}'
_OUTPUT_FILE_NAME = "output.md"


def test_convert_with_no_file() -> None:
    # Execute
    with pytest.raises(SystemExit):
        convert(output_file="some.md")


@patch.object(Path, "open", new_callable=mock_open(read_data=_JSON_DATA))
def test_convert_with_json_data(mock_open_file: Mock) -> None:
    # Prepare
    mock_open_file.return_value.__enter__.return_value = StringIO(_JSON_DATA)

    # Execute
    convert(output_file=_OUTPUT_FILE_NAME, json_file="test.json")

    # Assert
    mock_open_file.assert_any_call("r", encoding="utf-8")
    mock_open_file.assert_any_call("w", encoding="utf-8")


@patch.object(Path, "open", new_callable=mock_open())
def test_convert_with_yaml_data(mock_open_file: Mock) -> None:
    # Prepare
    data = "key: value"
    mock_open_file.return_value.__enter__.return_value = StringIO(data)

    # Execute
    convert(output_file=_OUTPUT_FILE_NAME, yaml_file="test.yaml")

    # Assert
    mock_open_file.assert_any_call("r", encoding="utf-8")
    mock_open_file.assert_any_call("w", encoding="utf-8")


@patch("yaml_to_markdown.convert.convert")
def test_main_parses_table_sections(mock_convert: Mock) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "-o",
            _OUTPUT_FILE_NAME,
            "-j",
            "test.json",
            "-t",
            "team members->Member,departments",
        ],
    )

    assert result.exit_code == 0
    mock_convert.assert_called_once_with(
        output_file=_OUTPUT_FILE_NAME,
        yaml_file=None,
        json_file="test.json",
        table_sections=["team members->Member", "departments"],
    )


@patch("yaml_to_markdown.convert.convert")
def test_main_parses_table_sections_with_whitespace(mock_convert: Mock) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        ["-o", _OUTPUT_FILE_NAME, "-j", "test.json", "-t", " people , departments "],
    )

    assert result.exit_code == 0
    mock_convert.assert_called_once_with(
        output_file=_OUTPUT_FILE_NAME,
        yaml_file=None,
        json_file="test.json",
        table_sections=["people", "departments"],
    )


@patch("yaml_to_markdown.convert.convert")
def test_main_without_table_sections(mock_convert: Mock) -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["-o", _OUTPUT_FILE_NAME, "-j", "test.json"])

    assert result.exit_code == 0
    mock_convert.assert_called_once_with(
        output_file=_OUTPUT_FILE_NAME,
        yaml_file=None,
        json_file="test.json",
        table_sections=None,
    )


@patch("yaml_to_markdown.convert.MDConverter")
@patch.object(Path, "open", new_callable=mock_open(read_data=_JSON_DATA))
def test_convert_passes_table_sections(
    mock_open_file: Mock, mock_md_converter_cls: Mock
) -> None:
    mock_open_file.return_value.__enter__.return_value = StringIO(_JSON_DATA)
    mock_converter = Mock()
    mock_md_converter_cls.return_value = mock_converter

    convert(
        output_file=_OUTPUT_FILE_NAME,
        json_file="test.json",
        table_sections=["people", "departments"],
    )

    mock_converter.set_table_sections.assert_called_once_with(["people", "departments"])
    mock_converter.convert.assert_called_once()


@patch("yaml_to_markdown.convert.MDConverter")
@patch.object(Path, "open", new_callable=mock_open(read_data=_JSON_DATA))
def test_convert_without_table_sections(
    mock_open_file: Mock, mock_md_converter_cls: Mock
) -> None:
    mock_open_file.return_value.__enter__.return_value = StringIO(_JSON_DATA)
    mock_converter = Mock()
    mock_md_converter_cls.return_value = mock_converter

    convert(output_file=_OUTPUT_FILE_NAME, json_file="test.json")

    mock_converter.set_table_sections.assert_not_called()
    mock_converter.convert.assert_called_once()
