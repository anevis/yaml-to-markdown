# YAML to Markdown Converter

A Python utility to take a JSON / YAML file or a python dict / list and create a Markdown file.

## Installation

```bash
pip install yaml-to-markdown
```

## Usage

```bash
$ yaml-to-markdown --help
Convert JSON or YAML to Markdown.
Usage: yaml-to-markdown -o <output_file> [-y <yaml_file> | -j <json_file>]
    -o, --output-file <output_file>: Path to the output file as a string [Mandatory].
    -y, --yaml-file <yaml_file>: Path to the YAML file as a string [Optional]
    -j, --json-file <json_file>: Path to the JSON file as a string [Optional]
    -h, --help: Show this message and exit.
Note: Either yaml_file or json_file is required along with output_file.
Example: yaml-to-markdown -o output.md -y data.yaml
```

### In Python Code example:

#### Convert a Pyton dictionary to Markdown:
```python
from yaml_to_markdown.md_converter import MDConverter

data = {
    "name": "John Doe",
    "age": 30,
    "city": "Sydney",
    "hobbies": ["reading", "swimming"],
}
converter = MDConverter()
with open("output.md", "w") as f:
    converter.convert(data, f)
```
Content of `output.md` file will be:
```markdown
## Name
John Doe
## Age
30
## City
Sydney
## Hobbies
* reading
* swimming
```

### From the Command Line

You can also use the command line interface to convert a JSON or YAML file to Markdown. Here's an example:

#### Convert a JSON file to Markdown:
```bash
yaml-to-markdown --output-file output.md --json-file test.json
```

#### Convert a YAML file to Markdown:
```bash
yaml-to-markdown --output-file output.md --yaml-file test.yaml
```

## Developer Guide
Please see the [DEVELOPER.md](docs/DEVELOPER.md) file for more information on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
