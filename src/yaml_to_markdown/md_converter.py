from __future__ import annotations

from typing import Any, Dict, IO, List, Optional, Union, Callable

from yaml_to_markdown.utils import convert_to_title_case


class MDConverter:
    def __init__(self) -> None:
        """
        Converter to convert a JSON object into Markdown.
        """
        self._sections: Optional[List[str]] = None
        self._custom_processors: Optional[
            Dict[str, Callable[[MDConverter, Optional[str], Any, int], str]]
        ] = None

    def set_selected_sections(self, sections: List[str]) -> None:
        """
        Set the sections (JSON keys) to include in the Markdown.
        By default, all sections will be included.

        Args:
            sections (List[str]): A list of section titles.
        """
        self._sections = sections

    def set_custom_section_processors(
        self,
        custom_processors: Dict[
            str, Callable[[MDConverter, Optional[str], Any, int], str]
        ],
    ):
        """
        Set custom section processors, the key must match a section name/key
        and the processor must take 4 arguments and return a Markdown string:
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
        data: Union[Dict[str, Union[List[Any], Dict[str, Any], str]], List[Any]],
        output_writer: IO[str],
    ) -> None:
        """
        Convert the given JSON object into Markdown.

        Args:
            data (Union[Dict[str, Union[List[Any], Dict[str, Any], str]], List[Any]]):
                The JSON object to convert, either a dictionary or a list.
            output_writer (IO[str]):
                The output stream object to write the Markdown to.
        """
        if isinstance(data, dict):
            self._process_dict(data, output_writer)
        elif isinstance(data, list):
            self._process_dict({None: data}, output_writer)

    def _process_dict(
        self,
        data: Dict[Optional[str], Any],
        output_writer: IO[str],
    ) -> None:
        for section in self._sections if self._sections is not None else data.keys():
            if section in data:
                output_writer.write(self.process_section(section, data.get(section)))

    def process_section(
        self,
        section: Optional[str],
        data: Union[List[Any], Dict[str, Any], str],
        level: int = 2,
    ) -> str:
        section_title = (
            f" {convert_to_title_case(section)}" if section is not None else ""
        )
        if self._custom_processors and section in self._custom_processors:
            section_str = self._custom_processors[section](self, section, data, level)
        elif isinstance(data, list):
            section_str = (
                f"{'#' * level}{section_title}\n{self._process_list(data=data)}"
            )
        elif isinstance(data, dict):
            section_str = f"{'#' * level}{section_title}\n"
            for section in data.keys():
                section_str += self.process_section(
                    section, data.get(section), level=level + 1
                )
        else:
            section_str = self._get_str(section, data, level)
        return f"{section_str}\n"

    def _process_list(self, data: List[Any]) -> str:
        if isinstance(data[0], dict):
            return self._process_table(data)
        elif isinstance(data[0], list):
            list_str = ""
            for item in data:
                list_str += f"{self._process_list(item)}\n"
            return list_str
        else:
            return "\n".join([f"* {item}" for item in data])

    def _process_table(self, data: List[Dict[str, str]]) -> str:
        columns = self._get_columns(data)
        table_str = self._process_columns(columns)
        for row in data:
            cell_data = [self._get_str(col, row.get(col, ""), -1) for col in columns]
            row_data = " | ".join(cell_data)
            table_str += f"\n| {row_data} |"
        return table_str

    @staticmethod
    def _process_columns(columns: List[str]) -> str:
        column_titles = " | ".join([convert_to_title_case(col) for col in columns])
        col_sep = " | ".join(["---" for _ in columns])
        return f"| {column_titles} |\n| {col_sep} |"

    @staticmethod
    def _get_columns(data: List[Dict[str, Any]]) -> List[str]:
        columns: List[str] = []
        for row in data:
            for col in row.keys():
                if col not in columns:
                    columns.append(col)
        return columns

    def _get_str(self, text: str, data: Any, level: int) -> str:
        str_data = str(data)
        prefix = "\n" if level > 0 else ""
        if isinstance(data, list):
            lst_str = "".join([f"<li>{item}</li>" for item in data])
            return f"<ul>{lst_str}</ul>"
        elif self._is_image(str_data):
            return f"{prefix}![{convert_to_title_case(text)}]({str_data})"
        elif self._is_link(str_data):
            return f"{prefix}[{convert_to_title_case(text)}]({str_data})"
        else:
            value = str_data.replace("\n", "<br/>")
            if level > 0:
                value = f"{'#' * level} {convert_to_title_case(text)}\n{value}"
            return value

    @staticmethod
    def _is_image(data: str) -> bool:
        file_ext = data.split(".")[-1]
        return file_ext and file_ext.lower() in ("png", "jpg", "jpeg", "gif", "svg")

    @staticmethod
    def _is_link(data: str) -> bool:
        file_ext = data.split(".")[-1]
        return (
            "\n" not in data
            and "." in data
            and file_ext is not None
            and (len(file_ext) == 4 or len(file_ext) == 3)
        ) or (
            data.lower().startswith("http")
            or data.lower().startswith("./")
            or data.lower().startswith("/")
        )
