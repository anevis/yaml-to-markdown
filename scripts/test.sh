#!/usr/bin/env bash
#
# This script is used to test python code.
set -euo pipefail

source "$(dirname "$0")/includes/init.sh"

python -m pytest -vvv --cov-config=.coveragerc --cov-report xml:output/coverage.xml --cov=. src/
