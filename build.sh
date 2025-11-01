#!/usr/bin/env bash
# Exit on error
set -o errexit

# Ensure Poetry uses the correct Python version
# Find Python 3.12 installed by Render (based on PYTHON_VERSION)
if [ -n "$PYTHON_VERSION" ]; then
    # Look for Python in Render's installation path
    PYTHON_MAJOR_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f1,2)
    PYTHON_FULL_PATH=""
    
    # Check Render's Python installation directory
    if [ -d "/opt/render/project/python" ]; then
        PYTHON_FULL_PATH=$(find /opt/render/project/python -type d -name "Python-$PYTHON_VERSION" -o -name "Python-$PYTHON_MAJOR_MINOR*" | head -1)
        if [ -n "$PYTHON_FULL_PATH" ] && [ -f "$PYTHON_FULL_PATH/bin/python" ]; then
            PYTHON_FULL_PATH="$PYTHON_FULL_PATH/bin/python"
        fi
    fi
    
    # Fallback to system python with version
    if [ -z "$PYTHON_FULL_PATH" ]; then
        if command -v "python$PYTHON_VERSION" &> /dev/null; then
            PYTHON_FULL_PATH=$(command -v "python$PYTHON_VERSION")
        elif command -v "python$PYTHON_MAJOR_MINOR" &> /dev/null; then
            PYTHON_FULL_PATH=$(command -v "python$PYTHON_MAJOR_MINOR")
        fi
    fi
fi

# Remove all existing Poetry environments to force recreation
if [ -d "$HOME/.cache/pypoetry/virtualenvs" ]; then
    rm -rf "$HOME/.cache/pypoetry/virtualenvs"/* 2>/dev/null || true
fi
if [ -d ".venv" ]; then
    rm -rf .venv 2>/dev/null || true
fi

# Set Poetry to use the correct Python
if [ -n "$PYTHON_FULL_PATH" ] && [ -f "$PYTHON_FULL_PATH" ]; then
    echo "Using Python: $PYTHON_FULL_PATH"
    poetry env use "$PYTHON_FULL_PATH"
elif command -v python3.12 &> /dev/null; then
    echo "Using Python: python3.12"
    poetry env use python3.12
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