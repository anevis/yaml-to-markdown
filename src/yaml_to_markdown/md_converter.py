from __future__ import annotations

import urllib.parse
from collections.abc import Callable
from pathlib import Path
from typing import IO, Any

from yaml_to_markdown.utils import convert_to_title_case


class MDConverter:
    def __init__(self) -> None:
        """Converter to convert a JSON object into Markdown."""
        self._sections: list[str] | None = None
        self._table_sections: dict[str, str] | None = None
        self._custom_processors: (
            dict[str, Callable[[MDConverter, str | None, Any, int], str]] | None
        ) = None

    def set_selected_sections(self, sections: list[str]) -> None:
        """Set the sections (JSON keys) to include in the Markdown.

        By default, all sections will be included.

        Args:
            sections (List[str]): A list of section titles.
        """
        self._sections = sections

    def set_table_sections(self, sections: list[str]) -> None:
        """Set sections whose dict children should render as table rows.

        Each subsection key becomes the first table column (title-cased, matching
        heading style). The column header is blank unless a title is given with
        ``section->Title`` syntax.

        Args:
            sections (List[str]): Section specs, e.g. ``["people"]`` or
                ``["team members->Member"]``.
        """
        parsed: dict[str, str] = {}
        for spec in sections:
            section_key, column_title = self._parse_table_section_spec(spec)
            parsed[section_key] = column_title
        self._table_sections = parsed

    @staticmethod
    def _parse_table_section_spec(spec: str) -> tuple[str, str]:
        if "->" in spec:
            section_key, column_title = spec.split("->", maxsplit=1)
            return section_key.strip(), column_title.strip()
        return spec.strip(), ""

    def set_custom_section_processors(
        self,
        custom_processors: dict[str, Callable[[MDConverter, str | None, Any, int], str]],
    ) -> None:
        """Set custom section processors.

        The key must match a section name/key and the processor must take
         4 arguments and return a Markdown string:
            converter (MDConverter): The current converter object.
            section ([str]): The section key
            data (Union[List[Any], Dict[str, Any], str]): The data for the section
            level (int): The section level

        Args:
            custom_processors ([Dict[Callable[[MDConverter, str, Any, int], str]]])
        """
        self._custom_processors = custom_processors

    def convert(
        self,
        data: (
            dict[str, str | list[Any] | list[dict[str, str]] | dict[str, Any]] | list[Any]
        ),
        output_writer: IO[str],
    ) -> None:
        """Convert the given JSON object into Markdown.

        Args:
            data (dict[str, str] | dict[str, list[Any]] | dict[str, list[dict[str, str]]]
             | dict[str, dict[str, Any]] | list[Any]):
                The JSON object to convert, either a dictionary or a list.
            output_writer (IO[str]):
                The output stream object to write the Markdown to.
        """
        if isinstance(data, dict):
            self._process_dict(data, output_writer)  # type: ignore
        elif isinstance(data, list):
            self._process_dict({None: data}, output_writer)

    def _process_dict(
        self,
        data: dict[str | None, str | list[Any] | list[dict[str, str]] | dict[str, Any]],
        output_writer: IO[str],
    ) -> None:
        for section in self._sections if self._sections is not None else data:
            if section in data:
                output_writer.write(self.process_section(section, data.get(section)))

    def process_section(
        self,
        section: str | None,
        data: Any | list[Any] | dict[str, Any] | str,
        level: int = 2,
    ) -> str:
        section_title = (
            f" {convert_to_title_case(section)}" if section is not None else ""
        )
        head_str = "#" * level
        if self._custom_processors and section in self._custom_processors:
            section_str = self._custom_processors[section](self, section, data, level)
        elif isinstance(data, list):
            section_str = f"{head_str}{section_title}\n{self._process_list(data=data)}"
        elif (
            isinstance(data, dict)
            and self._table_sections is not None
            and section in self._table_sections
        ):
            section_str = f"{head_str}{section_title}\n"
            key_column = self._table_sections[section]
            rows = self._dict_to_table_rows(data, key_column=key_column)
            if rows:
                section_str += self._process_table(
                    rows, literal_column_titles={key_column}
                )
        elif isinstance(data, dict):
            section_str = f"{head_str}{section_title}\n"
            for sec in data:
                section_str += self.process_section(sec, data.get(sec), level=level + 1)
        else:
            section_str = self._get_str(
                section if section is not None else "", data, level
            )
        return f"{section_str}\n"

    @staticmethod
    def _dict_to_table_rows(
        data: dict[str, Any], key_column: str = ""
    ) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for key, value in data.items():
            row = dict(value) if isinstance(value, dict) else {"value": value}
            rows.append({
                key_column: convert_to_title_case(str(key)),
                **{k: v for k, v in row.items() if k != key_column},
            })
        return rows

    def _process_list(self, data: list[Any]) -> str:
        if isinstance(data[0], dict):
            return self._process_table(data)
        if isinstance(data[0], list):
            list_str = ""
            for item in data:
                list_str += f"{self._process_list(item)}\n"
            return list_str
        return "\n".join([f"* {item}" for item in data])

    def _process_table(
        self,
        data: list[dict[str, Any]],
        literal_column_titles: set[str] | None = None,
    ) -> str:
        columns = self._get_columns(data)
        table_str = self._process_columns(columns, literal_column_titles)
        for row in data:
            cell_data = [self._get_str(col, row.get(col, ""), -1) for col in columns]
            row_data = " | ".join(cell_data)
            table_str += f"\n| {row_data} |"
        return table_str

    @staticmethod
    def _process_columns(
        columns: list[str], literal_column_titles: set[str] | None = None
    ) -> str:
        literal = literal_column_titles or set()
        titles: list[str] = []
        for col in columns:
            if col in literal:
                titles.append(col)
            else:
                titles.append(convert_to_title_case(col))
        column_titles = " | ".join(titles)
        col_sep = " | ".join(["---" for _ in columns])
        return f"| {column_titles} |\n| {col_sep} |"

    @staticmethod
    def _get_columns(data: list[dict[str, Any]]) -> list[str]:
        columns: list[str] = []
        for row in data:
            for col in row:
                if col not in columns:
                    columns.append(col)
        return columns

    def _get_str(self, text: str, data: Any, level: int) -> str:
        str_data = str(data)
        prefix = "\n" if level > 0 else ""
        if isinstance(data, dict):
            return "<br/>".join([
                f"{convert_to_title_case(str(key))}: {self._get_str(str(key), value, -1)}"
                for key, value in data.items()
            ])
        if isinstance(data, list):
            lst_str = "".join([f"<li>{item}</li>" for item in data])
            return f"<ul>{lst_str}</ul>"
        if self._is_image(str_data):
            return f"{prefix}![{convert_to_title_case(text)}]({str_data})"
        if self._is_link(str_data):
            return f"{prefix}[{convert_to_title_case(text)}]({str_data})"
        value = str_data.replace("\n", "<br/>")
        if level > 0:
            head_str = "#" * level
            value = f"{head_str} {convert_to_title_case(text)}\n{value}"
        return value

    def _is_image(self, data: str) -> bool:
        file_ext = self._get_file_ext(data)
        return file_ext is not None and file_ext.lower() in {
            "png",
            "jpg",
            "jpeg",
            "gif",
            "svg",
        }

    @staticmethod
    def _get_file_ext(data: str) -> str | None:
        if "." in data:
            return data.rsplit(".", maxsplit=1)[-1]
        return None

    def _is_link(self, data: str) -> bool:
        contains_no_newline = "\n" not in data

        if contains_no_newline and self._is_local_file(data):
            return True

        return contains_no_newline and self._is_valid_uri(data)

    @staticmethod
    def _is_local_file(file_path: str) -> bool:
        data_as_path = Path(file_path)

        try:
            if not data_as_path.is_file():
                return False
        except OSError:
            return False
        if not data_as_path.exists():
            return False

        is_relative = data_as_path.is_relative_to(".")
        is_explicitly_relative_to_current_directory = (
            is_relative and file_path.startswith("./")
        )

        return is_explicitly_relative_to_current_directory or data_as_path.is_absolute()

    @staticmethod
    def _is_valid_uri(uri: str) -> bool:
        data_as_uri = urllib.parse.urlparse(uri)
        return data_as_uri.scheme != "" and data_as_uri.netloc != ""  # ruff: ignore[compare-to-empty-string]
