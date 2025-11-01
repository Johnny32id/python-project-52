#!/usr/bin/env bash
# Exit on error
set -o errexit

# Ensure Poetry uses the correct Python version
# Remove any existing venv that might use wrong Python version
poetry env remove python3 2>/dev/null || true
poetry env remove python3.11 2>/dev/null || true

# Find and use the correct Python executable
if command -v python3.12 &> /dev/null; then
    poetry env use python3.12
elif [ -f /opt/render/project/python/Python-*/bin/python ]; then
    # Use Python installed by Render
    python_path=$(find /opt/render/project/python -name python -type f | head -1)
    if [ -n "$python_path" ]; then
        poetry env use "$python_path"
    fi
elif command -v python3 &> /dev/null; then
    poetry env use python3
fi

# Modify this line as needed for your package manager (pip, poetry, etc.)
make install

# Convert static asset files
make collectstatic

# Apply any outstanding database migrations
make migrate