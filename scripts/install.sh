#!/usr/bin/env bash
#
# This script is used to install python dependencies.
set -euo pipefail

source "$(dirname "$0")/includes/init.sh"

uv sync "$@"
