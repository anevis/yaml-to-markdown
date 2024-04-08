# Developer Documentation

## Getting Started

### Prerequisites

- devbox
- Python (3.12.2)
- pip

#### Setting up the Development Environment
Install the devbox CLI tool if you haven't already. You can install it using the following command:

```bash
curl -fsSL https://get.jetpack.io/devbox | bash
````

[![Built with Devbox](https://jetpack.io/img/devbox/shield_galaxy.svg)](https://jetpack.io/devbox/docs/contributor-quickstart/)
### Setting up Development Environment

#### Clone the repository:

```bash
git clone git@github.com:anevis/json-to-markdown.git

cd json-to-markdown-converter
```
#### Start the development environment:

```bash
devbox shell
```

#### Install the required packages:

From within devbox shell
```bash
pip install -r requirements.txt
```

From outside devbox shell
```bash
devbox run install
```

## Code Structure

The functionality can be used in the command line or in Python code.

To use the functionality in Python code, you can import the `MDConverter` class from the `yaml_to_markdown.md_converter` module.
The `md_converter.py` file contains the `MDConverter` class, which is used by the `convert` function to perform the conversion.

To use the functionality from the command line, you can run the `convert.py` script in the `yaml_to_markdown` directory.
This file contains the `convert` function, which takes a JSON or YAML file and converts it to Markdown.

## Testing
Tests for the project are located in the `*_test.py` files.
These tests use the Pytest and Mock libraries to test the functionality of the `convert` function and the `MDConverter` class.

### Running the Tests

You can run the tests with the following command:

From within devbox shell
```bash
pytest src/
```

From outside devbox shell
```bash
devbox run test
```
With Coverage, the coverage report will be generated in the `coverage.xml` file.
```bash
devbox run test-cov
```

## Linting & Formatting

The project uses the Black and Flake8 libraries for code formatting and linting.
You can run the following commands to format and lint the code:

From within devbox shell
```bash
black src/
flake8 src/
```

From outside devbox shell
```bash
devbox run format
devbox run lint
```

You can use `devbox run format-check` to check if the code is formatted correctly without making any changes.

## Contributing

We welcome contributions to this project. Please feel free to submit a pull request or open an issue on GitHub.

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
