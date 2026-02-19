#!/usr/bin/env bash
#
# This script is used to build the python package.
set -euo pipefail

set -a # ---- start exporting variables ----#

: "${RELEASE_VERSION:=1.0.dev}"
: "${BUILD_OUTPUT_DIR:=output/dist}"

set +a # ---- stop exporting variables ----#
