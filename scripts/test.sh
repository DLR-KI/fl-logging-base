#!/usr/bin/env bash
#
# SPDX-FileCopyrightText: 2026 German Aerospace Center (DLR)
# SPDX-License-Identifier: Apache-2.0
#
# cspell:ignore prek tput

# exit script if any command fails
set -e

# Helper to print step labels
print_step() {
  echo
  echo "$(tput bold)$1...$(tput sgr0)"
}

# pre commit on all files and changes (not only staged ones)
print_step "Pre-commit checks"
uv run prek run --all-files

# shell scripts
print_step "Shellcheck"
find scripts -type f -name "*.sh" -exec uv run shellcheck --external-sources --shell bash --source-path scripts {} +

# markdown
print_step "Markdown linting"
npm exec markdownlint-cli2 -- "./docs/**/*.md" "./README.md"

# static code checks (ruff: linter)
print_step "Ruff linter"
uv run ruff check src
if [[ -n $(find scripts -name "*.py[i]" -print -quit) ]]; then
  uv run ruff check scripts
fi
# static code checks (ruff: formatter)
print_step "Ruff formatter"
uv run ruff format --diff src
if [[ -n $(find scripts -name "*.py[i]" -print -quit) ]]; then
  uv run ruff format --diff scripts
fi

# static type checks (ty)
print_step "Type checks"
uv run ty check src
if [[ -n $(find scripts -name "*.py[i]" -print -quit) ]]; then
  uv run ty check scripts
fi

# static code analysis (pylint)
print_step "Pylint code analysis"
uv run pylint --fail-under=1 src
# uv run pylint --fail-under=8 src
# uv run pylint --exit-zero src scripts

# typo check (typos)
print_step "Typo check"
uv run typos

# license checks
print_step "License checks"
uv run licensecheck
uv run reuse lint

# vulnerability checks
print_step "Vulnerability checks"
uv audit

# success message
echo
echo "$(tput bold)Congratulations 🎉$(tput sgr0)"
echo "All tests successful."
