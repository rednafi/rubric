#!/usr/bin/env bash

# Run rubric without installing anything. To run this script remotely, execute:
# curl -s <url> | bash

# Bash strict mode.
set -euo pipefail

# Log color.
green="\033[0;32m"
clear="\033[0m"

python3 -m rubric.rubric $@
