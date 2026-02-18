#!/usr/bin/env bash
#
# This script is used to format python code.
set -euo pipefail

source "$(dirname "$0")/includes/init.sh"

echo "Format python code ..."
ruff format src "$@"
ruff check --fix src "$@"
