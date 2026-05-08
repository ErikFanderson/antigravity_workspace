#!/bin/zsh

# Get the directory where this script is located
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]:-${(%):-%x}}")" && pwd)"

# Set directory names (can be overridden by environment variables)
: ${PYENV_DIR:=".pyenv"}
: ${VENV_DIR:=".venv"}

# Set PYENV_ROOT to the local one in the repo
export PYENV_ROOT="$REPO_ROOT/$PYENV_DIR"
export PATH="$PYENV_ROOT/bin:$PATH"

# Initialize pyenv
if command -v pyenv &> /dev/null; then
    eval "$(pyenv init -)"
else
    echo "Warning: pyenv not found. Ensure it is installed."
fi

# Activate the virtual environment
if [ -d "$REPO_ROOT/$VENV_DIR" ]; then
    source "$REPO_ROOT/$VENV_DIR/bin/activate"
    # Ensure src is in PYTHONPATH (pip install -e . also handles this, but keeping for safety)
    export PYTHONPATH="$REPO_ROOT/src:$PYTHONPATH"
    echo "Python $(python --version) activated from local $PYENV_DIR and $VENV_DIR"
else
    echo "Virtual environment $VENV_DIR not found in $REPO_ROOT"
    echo "Run ./setup_env.sh to create it."
fi
