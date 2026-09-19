#!/usr/bin/env bash
#
# This script is used to Update app dependencies.
set -euo pipefail

source "$(dirname "$0")/includes/init.sh"

echo "Update Python dependencies ..."
uv sync --all-groups --upgrade
