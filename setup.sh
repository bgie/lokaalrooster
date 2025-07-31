#!/bin/bash
set -e

echo "Creating virtual environment..."
uv venv

echo "Installing dependencies..."
uv pip install -r requirements.txt

echo "Setup complete. Activate the environment with 'source .venv/bin/activate'"
