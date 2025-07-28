#!/usr/bin/env bash

set -e
set -x

mypy app --exclude venv
ruff check app
ruff format app --check
