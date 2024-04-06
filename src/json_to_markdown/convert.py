import io
import json
from typing import Dict, Any, Optional

import click
import yaml

from json_to_markdown.md_converter import MDConverter


def _get_json_data(json_file: str) -> Dict[str, Any]:
    with io.open(json_file, "r", encoding="utf-8") as j_file:
        return json.load(j_file)


def _get_yaml_data(yaml_file: str) -> Dict[str, Any]:
    with io.open(yaml_file, "r", encoding="utf-8") as y_file:
        return yaml.safe_load(y_file)


@click.command()
@click.option("-o", "--output-file", "output_file", type=str)
@click.option("-y", "--yaml-file", "yaml_file", type=str, default=None)
@click.option("-j", "--json-file", "json_file", type=str, default=None)
def main(output_file: str, yaml_file: Optional[str], json_file: Optional[str]) -> None:
    convert(output_file=output_file, yaml_file=yaml_file, json_file=json_file)


def convert(
    output_file: str, yaml_file: Optional[str] = None, json_file: Optional[str] = None
) -> None:
    if yaml_file is None and json_file is None:
        raise RuntimeError("One of yaml_file or json_file is required.")

    data = _get_json_data(json_file) if json_file else _get_yaml_data(yaml_file)
    with io.open(output_file, "w", encoding="utf-8") as md_file:
        converter = MDConverter()
        converter.set_selected_sections(
            sections=[
                "assessment-date",
                "assessors",
                "description",
                "diagram",
                "external-dependencies",
                "roles",
                "entry-points",
                "threats",
            ]
        )
        converter.convert(data=data, output_writer=md_file)


if __name__ == "__main__":
    main()
