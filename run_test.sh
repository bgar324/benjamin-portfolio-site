#!/bin/bash

set -euo pipefail

if [ -x "$PWD/python3-virtualenv/bin/python" ]; then
    "$PWD/python3-virtualenv/bin/python" -m unittest discover -v tests/
elif [ -x "$PWD/.venv/bin/python" ]; then
    "$PWD/.venv/bin/python" -m unittest discover -v tests/
else
    python3 -m unittest discover -v tests/
fi
