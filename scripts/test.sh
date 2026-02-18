#!/usr/bin/env bash
#
# This script is used to test python code.
set -euo pipefail

source "$(dirname "$0")/includes/init.sh"

python -m pytest -vvv --cov-config=.coveragerc --cov-report xml:output/coverage.xml --cov=. src/

if [[ -z "${GITHUB_APP_PEM_FILE:-}" && -z "${GITHUB_APP_PEM_FILE_PATH:-}" ]]; then
  echo "Skipping software configuration validation"
  exit
fi

if [[ "${BUILDKITE_BRANCH:-}" != "${BUILDKITE_PIPELINE_DEFAULT_BRANCH:-}" ]]; then
  CONFIG_DIRS=("config/ci" "config/deploy")
  for config_dir in "${CONFIG_DIRS[@]}"; do
    echo -e "\n--- ✅ Validate software configurations in '${config_dir}' ⚙️ ..."
    "${PWD}/scripts/validate.sh" "${config_dir}" "$@"
  done
fi
