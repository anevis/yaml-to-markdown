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

### YAML Conversion Examples

#### Simple Key-Value Pairs
**Input YAML:**
```yaml
name: John Doe
age: 30
city: Sydney
```
**Output Markdown:**
```markdown
## Name
John Doe
## Age
30
## City
Sydney
```

#### Lists
**Input YAML:**
```yaml
hobbies:
  - reading
  - swimming
  - cycling
```
**Output Markdown:**
```markdown
## Hobbies
* reading
* swimming
* cycling
```

#### Tables (List of Dictionaries)
**Input YAML:**
```yaml
employees:
  - name: Alice
    role: Developer
    department: Engineering
  - name: Bob
    role: Designer
    department: Creative
```
**Output Markdown:**
```markdown
## Employees
| Name | Role | Department |
| --- | --- | --- |
| Alice | Developer | Engineering |
| Bob | Designer | Creative |
```

#### Nested Structures
**Input YAML:**
```yaml
company:
  name: Tech Corp
  location: Sydney
  departments:
    engineering: 50
    sales: 30
```
**Output Markdown:**
```markdown
## Company
### Name
Tech Corp
### Location
Sydney
### Departments
#### Engineering
50
#### Sales
30
```

#### Images and Links
**Input YAML:**
```yaml
logo: company-logo.png
website: https://example.com
documentation: ./docs/guide.md
```
**Output Markdown:**
```markdown

![Logo](company-logo.png)

[Website](https://example.com)

[Documentation](./docs/guide.md)
```

**Note:** Files are only converted to links if they exist and are accessible. Invalid files, missing files, or files with permission errors are treated as normal text.

## Developer Guide
Please see the [DEVELOPER.md](docs/DEVELOPER.md) file for more information on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
