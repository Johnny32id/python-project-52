#!/usr/bin/env bash
# Exit on error
set -o errexit

# Ensure Poetry uses the correct Python version
# Find Python 3.12 installed by Render
PYTHON_312_PATH=""
if [ -d "/opt/render/project/python" ]; then
    PYTHON_312_PATH=$(find /opt/render/project/python -type f -name "python*3.12*" -o -path "*/Python-3.12*/bin/python" | head -1)
fi

if [ -z "$PYTHON_312_PATH" ] && command -v python3.12 &> /dev/null; then
    PYTHON_312_PATH=$(command -v python3.12)
fi

if [ -z "$PYTHON_312_PATH" ]; then
    # Fallback to any Python 3.12
    PYTHON_312_PATH=$(which python3.12 2>/dev/null || echo "")
fi

# Remove all existing Poetry environments to force recreation
if [ -d "$HOME/.cache/pypoetry/virtualenvs" ]; then
    rm -rf "$HOME/.cache/pypoetry/virtualenvs"/* 2>/dev/null || true
fi
if [ -d ".venv" ]; then
    rm -rf .venv 2>/dev/null || true
fi

# Set Poetry to use the correct Python
if [ -n "$PYTHON_312_PATH" ] && [ -f "$PYTHON_312_PATH" ]; then
    poetry env use "$PYTHON_312_PATH"
else
    echo "Warning: Python 3.12 not found, using default python3"
    poetry env use python3
fi

# Modify this line as needed for your package manager (pip, poetry, etc.)
make install

# Convert static asset files
make collectstatic

# Apply any outstanding database migrations
make migrate