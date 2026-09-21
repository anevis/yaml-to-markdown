# Developer Documentation

## Getting Started

### Prerequisites

- [devbox](https://www.jetify.com/devbox)
- Python >= 3.12 (devbox provides the pinned version)
- [uv](https://docs.astral.sh/uv/) (provided by the Devbox environment)

### Setting up the Development Environment

Install the Devbox CLI if you have not already:

```bash
curl -fsSL https://get.jetpack.io/devbox | bash
```

[![Built with Devbox](https://jetpack.io/img/devbox/shield_galaxy.svg)](https://jetpack.io/devbox/docs/contributor-quickstart/)

#### Clone the repository

```bash
git clone git@github.com:anevis/yaml-to-markdown.git
cd yaml-to-markdown
```

#### Start the development environment

```bash
devbox shell
```

#### Install the required packages

From within a Devbox shell:

```bash
uv sync
```

From outside a Devbox shell:

```bash
devbox run install
```

## Code Structure

The package lives under `src/yaml_to_markdown/`.

| Module | Role |
|--------|------|
| `md_converter.py` | `MDConverter` — converts a dict/list to Markdown |
| `convert.py` | CLI entry point (`yaml-to-markdown`) and file I/O helpers |
| `utils.py` | Shared helpers (e.g. title-case conversion) |

Python usage imports `MDConverter` from `yaml_to_markdown.md_converter`. The CLI is registered as `yaml-to-markdown` via the package entry point.

## Testing

Tests are colocated as `*_test.py` modules under `src/yaml_to_markdown/` and use Pytest.

### Running the tests

From within a Devbox shell:

```bash
pytest src/
```

From outside a Devbox shell:

```bash
devbox run test
```

`devbox run test` also writes a coverage report to `output/coverage.xml`.

## Linting and Formatting

The project uses [Ruff](https://docs.astral.sh/ruff/) for formatting and linting, and mypy for type checking.

From within a Devbox shell:

```bash
ruff format src/
ruff check src/
mypy --config-file=pyproject.toml src/
```

From outside a Devbox shell:

```bash
devbox run format
devbox run lint
```

## Updating Dependencies

To upgrade Python dependencies and refresh the lockfile:

```bash
devbox run update
```

This runs `uv sync --all-groups --upgrade`.

## Contributing

Contributions are welcome. Please open a pull request or an issue on GitHub.

## License

This project is licensed under the MIT License — see the [LICENSE](../LICENSE) file for details.
