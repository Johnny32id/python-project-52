#!/usr/bin/env bash
# Exit on error
set -o errexit

# Ensure Poetry uses the correct Python version
# Find the Python executable installed by Render
if command -v python3.12 &> /dev/null; then
    poetry env use python3.12
elif command -v python3 &> /dev/null; then
    poetry env use python3
elif [ -n "$PYTHON_VERSION" ]; then
    poetry env use "$PYTHON_VERSION"
fi

# Modify this line as needed for your package manager (pip, poetry, etc.)
make install

# Convert static asset files
make collectstatic

# Apply any outstanding database migrations
make migrate