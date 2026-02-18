#!/usr/bin/env bash
#
# This script is used to Upgrade app dependencies.
set -euo pipefail

source "$(dirname "$0")/includes/init.sh"

echo "Upgrade Python dependencies ..."
uv sync --all-groups --upgrade 
