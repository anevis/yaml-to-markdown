# YAML to Markdown Converter

A Python utility to take a JSON / YAML file or a python dict / list and create a Markdown file.

## Installation

```bash
pip install yaml-to-markdown
```

### Devbox (Nix flake)

```bash
devbox add github:anevis/yaml-to-markdown
```

Pin a release tag:

```bash
devbox add 'github:anevis/yaml-to-markdown/v1.0.1772518140'
```

Or add the same flake ref to the `packages` list in `devbox.json`. After `devbox shell`, `yaml-to-markdown` is on your `PATH`.

Local checkout:

```bash
devbox add path:./path/to/yaml-to-markdown
```

## Usage

```bash
$ yaml-to-markdown --help
Convert JSON or YAML to Markdown.
Usage: yaml-to-markdown -o <output_file> [-y <yaml_file> | -j <json_file>] [-t <table_sections>]
    -o, --output-file <output_file>: Path to the output file as a string [Mandatory].
    -y, --yaml-file <yaml_file>: Path to the YAML file as a string [Optional]
    -j, --json-file <json_file>: Path to the JSON file as a string [Optional]
    -t, --table-sections <table_sections>: Comma-separated section specs whose dict children render as table rows. Use section->Title to set the key-column header (blank by default) [Optional]
    -h, --help: Show this message and exit.
Note: Either yaml_file or json_file is required along with output_file.
Example: yaml-to-markdown -o output.md -y data.yaml
Example: yaml-to-markdown -o output.md -y data.yaml -t "team members->Member"
```

### In Python Code example:

#### Convert a Python dictionary to Markdown:
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

#### Select sections and custom processors

Include only specific top-level keys (and control their order):

```python
converter = MDConverter()
converter.set_selected_sections(["city", "name"])
```

Override rendering for a section key with a custom callback
`(converter, section, data, level) -> str`:

```python
def render_hobbies(converter, section, data, level):
    return f"{'#' * level} Hobbies\n" + "\n".join(f"- {item}" for item in data)

converter = MDConverter()
converter.set_custom_section_processors({"hobbies": render_hobbies})
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

Nested objects inside a table cell are shown as `Key: value` pairs, each on a new line (`<br/>`):

**Input YAML:**
```yaml
employees:
  - name: Alice
    contact:
      email: alice@example.com
      phone: "123"
```
**Output Markdown:**
```markdown
## Employees
| Name | Contact |
| --- | --- |
| Alice | Email: alice@example.com<br/>Phone: 123 |
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

#### Table Sections (Dict Children as Rows)
Mark section keys so their nested dict children become table rows. The subsection key is the first column (title-cased, like headings); its header is blank unless you set one with `section->Title`.

Section keys with spaces must be quoted in YAML and matched exactly when passed to `set_table_sections` or `-t`.

**Input YAML:**
```yaml
"team members":
  alice:
    role: Developer
    department: Engineering
  bob:
    role: Designer
    department: Creative
```

**Python (blank key-column header):**
```python
converter = MDConverter()
converter.set_table_sections(["team members"])
```

**CLI (with key-column header):**
```bash
yaml-to-markdown -o output.md -y data.yaml -t "team members->Member"
```

**Output Markdown** (`-t "team members"`):
```markdown
## Team Members
|  | Role | Department |
| --- | --- | --- |
| Alice | Developer | Engineering |
| Bob | Designer | Creative |
```

**Output Markdown** (`-t "team members->Member"`):
```markdown
## Team Members
| Member | Role | Department |
| --- | --- | --- |
| Alice | Developer | Engineering |
| Bob | Designer | Creative |
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
