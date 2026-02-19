#!/usr/bin/env bash
#
# This script is used to publish the python package.
set -euo pipefail

source "$(dirname "$0")/includes/init.sh"

echo "Publishing all files in ${BUILD_OUTPUT_DIR} to PyPi using uv ..."
uv publish "${BUILD_OUTPUT_DIR}/*"
