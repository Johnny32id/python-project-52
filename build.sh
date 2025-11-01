#!/usr/bin/env bash
# Exit on error
set -o errexit

# Ensure Poetry uses the correct Python version
if [ -n "$PYTHON_VERSION" ]; then
    python_path=$(which python3 || which python)
    poetry env use "$python_path" || poetry env use "$PYTHON_VERSION"
fi

# Modify this line as needed for your package manager (pip, poetry, etc.)
make install

# Convert static asset files
make collectstatic

# Apply any outstanding database migrations
make migrate