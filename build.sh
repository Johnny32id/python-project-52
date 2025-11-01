#!/usr/bin/env bash
# Exit on error
set -o errexit

# Ensure Poetry uses the correct Python version
# Remove Poetry's own venv that might use wrong Python version
if [ -d "/opt/render/project/poetry/venv" ]; then
    echo "Removing Poetry's venv with wrong Python version..."
    rm -rf /opt/render/project/poetry/venv 2>/dev/null || true
fi

# Remove all existing Poetry environments to force recreation
if [ -d "$HOME/.cache/pypoetry/virtualenvs" ]; then
    rm -rf "$HOME/.cache/pypoetry/virtualenvs"/* 2>/dev/null || true
fi
if [ -d ".venv" ]; then
    rm -rf .venv 2>/dev/null || true
fi

# Find Python 3.12 installed by Render
PYTHON_312_PATH=""
if [ -d "/opt/render/project/python" ]; then
    # Look for Python 3.12.x directory
    PYTHON_DIR=$(find /opt/render/project/python -maxdepth 1 -type d -name "Python-3.12*" | head -1)
    if [ -n "$PYTHON_DIR" ] && [ -f "$PYTHON_DIR/bin/python" ]; then
        PYTHON_312_PATH="$PYTHON_DIR/bin/python"
    fi
fi

# Fallback to system python3.12
if [ -z "$PYTHON_312_PATH" ]; then
    if command -v python3.12 &> /dev/null; then
        PYTHON_312_PATH=$(command -v python3.12)
    fi
fi

# Set Poetry to use the correct Python
if [ -n "$PYTHON_312_PATH" ] && [ -f "$PYTHON_312_PATH" ]; then
    echo "Using Python: $PYTHON_312_PATH"
    poetry env use "$PYTHON_312_PATH" --force
else
    echo "Warning: Python 3.12 not found, using default python3"
    poetry env use python3 --force
fi

# Modify this line as needed for your package manager (pip, poetry, etc.)
make install

# Convert static asset files
make collectstatic

# Apply any outstanding database migrations
make migrate