from __future__ import annotations

from collections.abc import Callable
from typing import IO, Any

from yaml_to_markdown.utils import convert_to_title_case


class MDConverter:
    def __init__(self) -> None:
        """Converter to convert a JSON object into Markdown."""
        self._sections: list[str] | None = None
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

    def set_custom_section_processors(
        self,
        custom_processors: dict[
            str, Callable[[MDConverter, str | None, Any, int], str]
        ],
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
            dict[str, str | list[Any] | list[dict[str, str]] | dict[str, Any]]
            | list[Any]
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
        elif isinstance(data, dict):
            section_str = f"{head_str}{section_title}\n"
            for sec in data:
                section_str += self.process_section(sec, data.get(sec), level=level + 1)
        else:
            section_str = self._get_str(
                section if section is not None else "", data, level
            )
        return f"{section_str}\n"

    def _process_list(self, data: list[Any]) -> str:
        if isinstance(data[0], dict):
            return self._process_table(data)
        if isinstance(data[0], list):
            list_str = ""
            for item in data:
                list_str += f"{self._process_list(item)}\n"
            return list_str
        return "\n".join([f"* {item}" for item in data])

    def _process_table(self, data: list[dict[str, str]]) -> str:
        columns = self._get_columns(data)
        table_str = self._process_columns(columns)
        for row in data:
            cell_data = [self._get_str(col, row.get(col, ""), -1) for col in columns]
            row_data = " | ".join(cell_data)
            table_str += f"\n| {row_data} |"
        return table_str

    @staticmethod
    def _process_columns(columns: list[str]) -> str:
        column_titles = " | ".join([convert_to_title_case(col) for col in columns])
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

    @staticmethod
    def _is_image(data: str) -> bool:
        file_ext = data.split(".")[-1]
        return file_ext is not None and file_ext.lower() in {
            "png",
            "jpg",
            "jpeg",
            "gif",
            "svg",
        }

    @staticmethod
    def _is_link(data: str) -> bool:
        file_ext = data.split(".")[-1]
        min_file_ext_len = 3
        max_file_ext_len = 4
        return (
            "\n" not in data
            and "." in data
            and file_ext is not None
            and (len(file_ext) == max_file_ext_len or len(file_ext) == min_file_ext_len)
        ) or (
            data.lower().startswith("http")
            or data.lower().startswith("./")
            or data.lower().startswith("/")
        )
