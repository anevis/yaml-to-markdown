from io import StringIO
from pathlib import Path
from unittest.mock import Mock, mock_open, patch

import pytest

from yaml_to_markdown.convert import _parse_table_sections, convert

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


def test_parse_table_sections() -> None:
    assert _parse_table_sections(None) is None
    assert _parse_table_sections("") is None
    assert _parse_table_sections("  ,  ") is None
    assert _parse_table_sections("people") == ["people"]
    assert _parse_table_sections("people,departments") == ["people", "departments"]
    assert _parse_table_sections(" people , departments ") == ["people", "departments"]
    assert _parse_table_sections("team members->Member") == ["team members->Member"]
    assert _parse_table_sections("team members->Member,departments") == [
        "team members->Member",
        "departments",
    ]


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

    mock_converter.set_table_sections.assert_called_once_with(
        ["people", "departments"]
    )
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
