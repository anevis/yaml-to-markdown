# YAML to Markdown Converter

A Python utility to take a JSON / YAML file or a python dict / list and create a Markdown file.

## Usage

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
python yaml_to_markdown/convert.py --output-file output.md --json-file test.json
```

#### Convert a YAML file to Markdown:
```bash
python yaml_to_markdown/convert.py --output-file output.md --yaml-file test.yaml
```

## Developer Guide
Please see the [DEVELOPER.md](docs/DEVELOPER.md) file for more information on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
