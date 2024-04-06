from io import StringIO
from unittest.mock import mock_open, patch, Mock

import pytest

from yaml_to_markdown.convert import convert

_JSON_DATA = '{"key": "value"}'


def test_convert_with_no_file() -> None:
    # Execute
    with pytest.raises(
        RuntimeError, match="One of yaml_file or json_file is required."
    ):
        convert(output_file="some.md")


@patch("io.open", new_callable=mock_open(read_data=_JSON_DATA))
def test_convert_with_json_data(mock_open_file: Mock) -> None:
    # Prepare
    mock_open_file.return_value.__enter__.return_value = StringIO(_JSON_DATA)

    # Execute
    convert(output_file="output.md", json_file="test.json")

    # Assert
    mock_open_file.assert_any_call("test.json", "r", encoding="utf-8")
    mock_open_file.assert_any_call("output.md", "w", encoding="utf-8")


@patch("io.open", new_callable=mock_open())
def test_convert_with_yaml_data(mock_open_file: Mock) -> None:
    # Prepare
    data = "key: value"
    mock_open_file.return_value.__enter__.return_value = StringIO(data)

    # Execute
    convert(output_file="output.md", yaml_file="test.yaml")

    # Assert
    mock_open_file.assert_any_call("test.yaml", "r", encoding="utf-8")
    mock_open_file.assert_any_call("output.md", "w", encoding="utf-8")
