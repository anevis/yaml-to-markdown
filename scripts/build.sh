#!/usr/bin/env bash
#
# This script is used to build the python package.
set -euo pipefail

source "$(dirname "$0")/includes/init.sh"

echo "Package version: ${RELEASE_VERSION}"
echo "__version__ = '${RELEASE_VERSION}'" > src/version.py

echo "Building package ..."
rm -rf "${BUILD_OUTPUT_DIR}/*"

uv build --sdist --wheel --out-dir="${BUILD_OUTPUT_DIR}"

# Clean up
rm -rf build
rm -rf src/*.egg-info
rm -rf out
