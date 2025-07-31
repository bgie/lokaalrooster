#!/bin/bash
set -e

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate the virtual environment
source .venv/bin/activate

# Run the Flask application
echo "Starting Flask app on http://127.0.0.1:5000"
python app.py
