#!/bin/zsh

# Default values
PYENV_DIR=".pyenv"
VENV_DIR=".venv"
PYTHON_VERSION=$(cat .python-version 2>/dev/null || echo "3.14.4")

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --pyenv-dir)
      PYENV_DIR="$2"
      shift 2
      ;;
    --venv-dir)
      VENV_DIR="$2"
      shift 2
      ;;
    --python-version)
      PYTHON_VERSION="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]:-${(%):-%x}}")" && pwd)"
ABS_PYENV_DIR="$REPO_ROOT/$PYENV_DIR"
ABS_VENV_DIR="$REPO_ROOT/$VENV_DIR"

# Set PYENV_ROOT to the specified local directory
export PYENV_ROOT="$ABS_PYENV_DIR"
export PATH="$PYENV_ROOT/bin:$PATH"

# Ensure pyenv is installed
if ! command -v pyenv &> /dev/null; then
    echo "Error: pyenv not found. Please install it first (e.g., 'brew install pyenv')."
    exit 1
fi

eval "$(pyenv init -)"

# Install Python version if not present locally
if ! pyenv versions --bare | grep -q "^$PYTHON_VERSION$"; then
    echo "Installing Python $PYTHON_VERSION into $PYENV_DIR..."
    pyenv install "$PYTHON_VERSION"
else
    echo "Python $PYTHON_VERSION is already installed in $PYENV_DIR."
fi

# Set local version
pyenv local "$PYTHON_VERSION"

# Create/Update virtual environment
if [ ! -d "$ABS_VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR..."
    python -m venv "$ABS_VENV_DIR"
else
    echo "Virtual environment already exists in $VENV_DIR."
fi

# Activate and install dependencies
source "$ABS_VENV_DIR/bin/activate"

echo "Installing/Updating dependencies from pyproject.toml..."
pip install --upgrade pip
# Install dependencies from pyproject.toml
# Using -e . ensures the src/ directory is in the path and dependencies are installed
pip install -e .

echo "------------------------------------------------"
echo "Setup complete!"
echo "To activate this environment, run: source activate_all.sh"
echo " (Note: If you used custom directory names, update activate_all.sh accordingly)"
