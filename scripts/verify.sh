#!/usr/bin/env bash
#
# This script is used to verify python code by linting, type checking and checking dependencies.
set -euo pipefail

echo "Linting python code ..."
devbox run lint

echo "Type checking python code ..."
devbox run type-check

echo "Checking dependencies of python code ..."
devbox run audit
