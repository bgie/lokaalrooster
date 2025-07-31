#!/bin/bash
set -e

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate the virtual environment
source .venv/bin/activate

echo "Formatting code with ruff..."
ruff format .

echo "Linting code with ruff..."
ruff check .

echo "Linting and formatting complete."
