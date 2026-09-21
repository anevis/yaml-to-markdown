from copy import deepcopy
from io import StringIO
from typing import Any
from unittest import mock
from unittest.mock import Mock

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


def test_process_list() -> None:
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


def test_process_list_of_list() -> None:
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


def test_process_section_with_str() -> None:
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


def test_process_section_with_list_str() -> None:
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


def test_process_section_with_list_dict() -> None:
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


def test_process_section_with_list_list() -> None:
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


def test_process_section_skip_section() -> None:
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
def test_process_section(extra_item: dict[str, Any], expected_output: str) -> None:
    output_writer = StringIO()
    md_converter = MDConverter()
    table_items = [deepcopy(itm) for itm in _TABLE_ITEMS]
    table_items.append(extra_item)
    data: dict[str, Any] = {
        "section-one": table_items,
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


def test_process_section_with_image() -> None:
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


def test_process_section_with_http_link() -> None:
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


@mock.patch("yaml_to_markdown.md_converter.Path")
def test_process_section_with_relative_link(mock_path: Mock) -> None:
    def _path_side_effect(path_str: str) -> Mock:
        path_instance = Mock()
        value = path_str != "My section" and not path_str.endswith(".net")
        path_instance.exists.return_value = value
        path_instance.is_file.return_value = value
        path_instance.is_relative_to.return_value = value
        return path_instance

    mock_path.side_effect = _path_side_effect
    output_writer = StringIO()
    md_converter = MDConverter()
    data: dict[str, Any] = {
        "section0": "My section",
        "section1": "./something.puml",
        "section2": "/dit/something.puml",
        "section3": "something.puml",
        "section4": "designation-identity.company-intra.net",
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
## Section4
designation-identity.company-intra.net
"""
    )


def test_process_section_with_long_value() -> None:
    long_str = (
        "somethingsomethingsomethingsomethingsomethingsomething"
        "somethingsomethingsomethingsomethingsomethingsomething"
        "somethingsomethingsomethingsomethingsomethingsomething"
        "somethingsomethingsomethingsomethingsomethingsomething"
        "somethingsomethingsomethingsomethingsomethingsomething"
        "somethingsomethingsomethingsomethingsomethingsomething"
    )
    output_writer = StringIO()
    md_converter = MDConverter()
    data: dict[str, Any] = {"section": long_str}
    md_converter.convert(data, output_writer)
    output = output_writer.getvalue()

    assert (
        output
        == f"""## Section
{long_str}
"""
    )


@mock.patch("yaml_to_markdown.md_converter.Path")
def test_process_section_with_relative_link_no_file(mock_path: Mock) -> None:
    path_instance = Mock()
    path_instance.exists.return_value = False
    path_instance.is_file.return_value = True

    mock_path.return_value = path_instance
    output_writer = StringIO()
    md_converter = MDConverter()
    data: dict[str, Any] = {"section": "./something.puml"}
    md_converter.convert(data, output_writer)
    output = output_writer.getvalue()

    assert (
        output
        == """## Section
./something.puml
"""
    )


def test_process_section_different_section_order() -> None:
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


def test_process_section_with_dict() -> None:
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


def test_process_section_custom_processor() -> None:
    section_name = "custom"
    section_value = ["data1"]
    output_writer = StringIO()
    mock_function = Mock(return_value="")
    md_converter = MDConverter()
    md_converter.set_custom_section_processors(
        custom_processors={section_name: mock_function}
    )
    data: dict[str, Any] = {section_name: section_value}
    md_converter.convert(data, output_writer)
    output_writer.getvalue()

    mock_function.assert_called_once_with(md_converter, section_name, section_value, 2)


def test_process_table_sections_dict_of_dicts() -> None:
    output_writer = StringIO()
    md_converter = MDConverter()
    md_converter.set_table_sections(["people"])
    data: dict[str, Any] = {
        "people": {
            "alice": {"role": "Developer", "department": "Engineering"},
            "bob": {"role": "Designer", "department": "Creative"},
        }
    }
    md_converter.convert(data, output_writer)
    output = output_writer.getvalue()

    assert (
        output
        == """## People
|  | Role | Department |
| --- | --- | --- |
| Alice | Developer | Engineering |
| Bob | Designer | Creative |
"""
    )


def test_process_table_sections_with_column_title() -> None:
    output_writer = StringIO()
    md_converter = MDConverter()
    md_converter.set_table_sections(["team members->Member"])
    data: dict[str, Any] = {
        "team members": {
            "alice": {"role": "Developer", "department": "Engineering"},
            "bob": {"role": "Designer", "department": "Creative"},
        }
    }
    md_converter.convert(data, output_writer)
    output = output_writer.getvalue()

    assert (
        output
        == """## Team Members
| Member | Role | Department |
| --- | --- | --- |
| Alice | Developer | Engineering |
| Bob | Designer | Creative |
"""
    )


def test_process_table_sections_nested_name_preserved() -> None:
    output_writer = StringIO()
    md_converter = MDConverter()
    md_converter.set_table_sections(["people"])
    data: dict[str, Any] = {
        "people": {
            "alice": {"name": "Alice Smith", "role": "Developer"},
        }
    }
    md_converter.convert(data, output_writer)
    output = output_writer.getvalue()

    assert (
        output
        == """## People
|  | Name | Role |
| --- | --- | --- |
| Alice | Alice Smith | Developer |
"""
    )


def test_process_table_sections_scalar_children() -> None:
    output_writer = StringIO()
    md_converter = MDConverter()
    md_converter.set_table_sections(["people"])
    data: dict[str, Any] = {
        "people": {
            "alice": "Developer",
            "bob": "Designer",
        }
    }
    md_converter.convert(data, output_writer)
    output = output_writer.getvalue()

    assert (
        output
        == """## People
|  | Value |
| --- | --- |
| Alice | Developer |
| Bob | Designer |
"""
    )


def test_process_table_sections_empty_dict() -> None:
    output_writer = StringIO()
    md_converter = MDConverter()
    md_converter.set_table_sections(["people"])
    data: dict[str, Any] = {"people": {}}
    md_converter.convert(data, output_writer)
    output = output_writer.getvalue()

    assert (
        output
        == """## People

"""
    )


def test_process_table_sections_nested_match() -> None:
    output_writer = StringIO()
    md_converter = MDConverter()
    md_converter.set_table_sections(["departments"])
    data: dict[str, Any] = {
        "company": {
            "name": "Tech Corp",
            "departments": {
                "engineering": {"headcount": 50},
                "sales": {"headcount": 30},
            },
        }
    }
    md_converter.convert(data, output_writer)
    output = output_writer.getvalue()

    assert (
        output
        == """## Company
### Name
Tech Corp
### Departments
|  | Headcount |
| --- | --- |
| Engineering | 50 |
| Sales | 30 |

"""
    )


def test_process_table_cell_with_nested_object() -> None:
    output_writer = StringIO()
    md_converter = MDConverter()
    data: dict[str, Any] = {
        "employees": [
            {
                "name": "Alice",
                "contact": {"email": "alice@example.com", "phone": "123"},
            },
            {
                "name": "Bob",
                "contact": {"email": "bob@example.com", "phone": "456"},
            },
        ]
    }
    md_converter.convert(data, output_writer)
    output = output_writer.getvalue()

    assert (
        output
        == """## Employees
| Name | Contact |
| --- | --- |
| Alice | Email: alice@example.com<br/>Phone: 123 |
| Bob | Email: bob@example.com<br/>Phone: 456 |
"""
    )


def test_process_table_sections_cell_with_nested_object() -> None:
    output_writer = StringIO()
    md_converter = MDConverter()
    md_converter.set_table_sections(["people"])
    data: dict[str, Any] = {
        "people": {
            "alice": {
                "role": "Developer",
                "contact": {"email": "alice@example.com", "city": "Sydney"},
            },
        }
    }
    md_converter.convert(data, output_writer)
    output = output_writer.getvalue()

    assert (
        output
        == """## People
|  | Role | Contact |
| --- | --- | --- |
| Alice | Developer | Email: alice@example.com<br/>City: Sydney |
"""
    )


def test_process_table_sections_spec_trims_whitespace() -> None:
    output_writer = StringIO()
    md_converter = MDConverter()
    md_converter.set_table_sections([" people -> Name "])
    data: dict[str, Any] = {
        "people": {
            "alice": {"role": "Developer"},
        }
    }
    md_converter.convert(data, output_writer)
    output = output_writer.getvalue()

    assert (
        output
        == """## People
| Name | Role |
| --- | --- |
| Alice | Developer |
"""
    )
