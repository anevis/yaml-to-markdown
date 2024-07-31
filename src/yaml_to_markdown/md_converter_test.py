from copy import deepcopy
from io import StringIO
from typing import Any
from unittest import mock

import pytest

from yaml_to_markdown.md_converter import MDConverter

_TABLE_ITEMS = [
    {
        "col1": "R1C1",
        "col2": "R1C2",
    },
    {
        "col1": "R2C1",
        "col2": "R2C2",
    },
]
_LIST_ITEMS = ["data1", "data2"]


class TestMDConverter:
    def test_process_list(self) -> None:
        output_writer = StringIO()
        md_converter = MDConverter()
        data = [{"section1": "data1"}]

        md_converter.convert(data, output_writer)
        output = output_writer.getvalue()

        assert (
            output
            == """##
| Section1 |
| --- |
| data1 |
"""
        )

    def test_process_list_of_list(self) -> None:
        output_writer = StringIO()
        md_converter = MDConverter()
        data = [
            ["list1 data1", "list1 data2"],
            ["list2 data1", "list2 data2"],
        ]

        md_converter.convert(data, output_writer)
        output = output_writer.getvalue()

        assert (
            output
            == """##
* list1 data1
* list1 data2
* list2 data1
* list2 data2

"""
        )

    def test_process_section_with_str(self) -> None:
        output_writer = StringIO()
        md_converter = MDConverter()
        data: dict[str, Any] = {"section1": "data1"}

        md_converter.convert(data, output_writer)
        output = output_writer.getvalue()

        assert (
            output
            == """## Section1
data1
"""
        )

    def test_process_section_with_list_str(self) -> None:
        output_writer = StringIO()
        md_converter = MDConverter()
        data: dict[str, Any] = {"section1": _LIST_ITEMS}
        md_converter.convert(data, output_writer)
        output = output_writer.getvalue()

        assert (
            output
            == """## Section1
* data1
* data2
"""
        )

    def test_process_section_with_list_dict(self) -> None:
        output_writer = StringIO()
        md_converter = MDConverter()
        data: dict[str, Any] = {"section1": _TABLE_ITEMS}
        md_converter.convert(data, output_writer)
        output = output_writer.getvalue()

        assert (
            output
            == """## Section1
| Col1 | Col2 |
| --- | --- |
| R1C1 | R1C2 |
| R2C1 | R2C2 |
"""
        )

    def test_process_section_with_list_list(self) -> None:
        output_writer = StringIO()
        md_converter = MDConverter()
        data: dict[str, Any] = {
            "section1": [
                ["R1C1", "R1C2"],
                ["R2C1", "R2C2"],
            ]
        }
        md_converter.convert(data, output_writer)
        output = output_writer.getvalue()

        assert (
            output
            == """## Section1
* R1C1
* R1C2
* R2C1
* R2C2

"""
        )

    def test_process_section_skip_section(self) -> None:
        output_writer = StringIO()
        md_converter = MDConverter()
        md_converter.set_selected_sections(["sec-two"])
        data: dict[str, Any] = {"sec-one": "First section", "sec-two": "Second Section"}
        md_converter.convert(data, output_writer)
        output = output_writer.getvalue()

        assert (
            output
            == """## Sec Two
Second Section
"""
        )

    @pytest.mark.parametrize(
        ("extra_item", "expected_output"),
        [
            (
                {
                    "col1": "R3C1",
                    "col2": "R3C2",
                    "column three": """R3C3
Line 2
Line 3""",
                },
                "| R3C1 | R3C2 | R3C3<br/>Line 2<br/>Line 3 |",
            ),
            (
                {
                    "col1": "R4C1",
                    "col2": "R4C2",
                    "column three": "R4C3",
                },
                "| R4C1 | R4C2 | R4C3 |",
            ),
            (
                {
                    "col1": "R5C1",
                    "col2": "R5C2",
                    "column three": ["R5C3", "R5C4"],
                },
                "| R5C1 | R5C2 | <ul><li>R5C3</li><li>R5C4</li></ul> |",
            ),
            (
                {
                    "col1": "R5C1",
                    "column three": "R5C3",
                },
                "| R5C1 |  | R5C3 |",
            ),
        ],
    )
    def test_process_section(
        self, extra_item: dict[str, Any], expected_output: str
    ) -> None:
        output_writer = StringIO()
        md_converter = MDConverter()
        _table_items = [deepcopy(itm) for itm in _TABLE_ITEMS]
        _table_items.append(extra_item)
        data: dict[str, Any] = {
            "section-one": _table_items,
            "section-two": _LIST_ITEMS,
        }
        md_converter.convert(data, output_writer)
        output = output_writer.getvalue()

        assert (
            output
            == f"""## Section One
| Col1 | Col2 | Column Three |
| --- | --- | --- |
| R1C1 | R1C2 |  |
| R2C1 | R2C2 |  |
{expected_output}
## Section Two
* data1
* data2
"""
        )

    def test_process_section_with_image(self) -> None:
        output_writer = StringIO()
        md_converter = MDConverter()
        data: dict[str, Any] = {"section1": "something.png"}
        md_converter.convert(data, output_writer)
        output = output_writer.getvalue()

        assert (
            output
            == """
![Section1](something.png)
"""
        )

    def test_process_section_with_http_link(self) -> None:
        output_writer = StringIO()
        md_converter = MDConverter()
        data: dict[str, Any] = {"section1": "https://something.html"}
        md_converter.convert(data, output_writer)
        output = output_writer.getvalue()

        assert (
            output
            == """
[Section1](https://something.html)
"""
        )

    def test_process_section_with_relative_link(self) -> None:
        output_writer = StringIO()
        md_converter = MDConverter()
        data: dict[str, Any] = {
            "section0": "My section",
            "section1": "./something.puml",
            "section2": "/dit/something.puml",
            "section3": "something.puml",
        }
        md_converter.convert(data, output_writer)
        output = output_writer.getvalue()

        assert (
            output
            == """## Section0
My section

[Section1](./something.puml)

[Section2](/dit/something.puml)

[Section3](something.puml)
"""
        )

    def test_process_section_different_section_order(self) -> None:
        output_writer = StringIO()
        md_converter = MDConverter()
        md_converter.set_selected_sections(["s3", "s2", "s1", "s4"])
        data: dict[str, Any] = {
            "s1": "Sec 1",
            "s2": "Sec 2",
            "s3": "Sec 3",
        }
        md_converter.convert(data, output_writer)
        output = output_writer.getvalue()

        assert (
            output
            == """## S3
Sec 3
## S2
Sec 2
## S1
Sec 1
"""
        )

    def test_process_section_with_dict(self) -> None:
        output_writer = StringIO()
        md_converter = MDConverter()
        data: dict[str, Any] = {"section1": {"key1": "value1", "key2": "value2"}}
        md_converter.convert(data, output_writer)
        output = output_writer.getvalue()

        assert (
            output
            == """## Section1
### Key1
value1
### Key2
value2

"""
        )

    def test_process_section_custom_processor(self) -> None:
        section_name = "custom"
        section_value = ["data1"]
        output_writer = StringIO()
        mock_function = mock.Mock(return_value="")
        md_converter = MDConverter()
        md_converter.set_custom_section_processors(
            custom_processors={section_name: mock_function}
        )
        data: dict[str, Any] = {section_name: section_value}
        md_converter.convert(data, output_writer)
        output_writer.getvalue()

        mock_function.assert_called_once_with(
            md_converter, section_name, section_value, 2
        )


def test_dummy() -> None:
    data: dict[str, Any] = {
        "name": "John Doe",
        "age": 30,
        "city": "Sydney",
        "hobbies": ["reading", "swimming"],
    }
    str_io = StringIO()
    md_converter = MDConverter()
    md_converter.convert(data, str_io)

    print(str_io.getvalue())
