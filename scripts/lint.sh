#!/usr/bin/env bash
#
# This script is used to lint python code.
set -euo pipefail

source "$(dirname "$0")/includes/init.sh"

echo "Linting python code ..."
ruff check src "$@"

echo "Type checking python code ..."
mypy --config-file="pyproject.toml" src/ "$@"
