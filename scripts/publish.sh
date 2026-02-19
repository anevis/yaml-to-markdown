#!/usr/bin/env bash
#
# This script is used to publish the python package.
set -euo pipefail

source "$(dirname "$0")/includes/init.sh"

log "Publishing all files in ${BUILD_OUTPUT_DIR} to ${artifact_path}/ using uv ..."
uv publish --publish-url "${ARTIFACTORY_URL}/api/pypi/iress-pypi" "${BUILD_OUTPUT_DIR}/*"
