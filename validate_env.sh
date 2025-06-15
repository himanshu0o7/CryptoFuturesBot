#!/bin/bash

# validate_env.sh: Validates the environment for CryptoFuturesBot

# Check if running in a virtual environment
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "Error: Not running in a virtual environment. Please activate the venv."
    echo "Run: source venv/bin/activate"
    exit 1
else
    echo "Virtual environment active: $VIRTUAL_ENV"
fi

# Check if config.env exists
CONFIG_FILE="config.env"
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "Error: $CONFIG_FILE not found in $(pwd)"
    exit 1
else
    echo "Found $CONFIG_FILE"
fi

# Source the config.env file
source "$CONFIG_FILE"

# List of required environment variables
REQUIRED_VARS=(
    "API_KEY"
    "API_SECRET"
    # Add other required variables for your bot, e.g., "COINSWITCH_ENDPOINT"
)

# Check if required environment variables are set
for var in "${REQUIRED_VARS[@]}"; do
    if [[ -z "${!var}" ]]; then
        echo "Error: Environment variable $var is not set."
        exit 1
    else
        echo "Environment variable $var is set."
    fi
done

# Check if Python is installed and version is compatible
PYTHON_MIN_VERSION="3.8"
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
if [[ -z "$PYTHON_VERSION" ]]; then
    echo "Error: Python not found."
    exit 1
fi
if [[ "$(printf '%s\n' "$PYTHON_VERSION" "$PYTHON_MIN_VERSION" | sort -V | head -n1)" != "$PYTHON_MIN_VERSION" ]]; then
    echo "Error: Python version $PYTHON_VERSION is less than required version $PYTHON_MIN_VERSION."
    exit 1
else
    echo "Python version $PYTHON_VERSION is compatible."
fi

# Check if required Python packages are installed
REQUIRED_PACKAGES=(
    "requests"
    "pandas"
    # Add other packages your bot depends on, e.g., "ccxt"
)

for pkg in "${REQUIRED_PACKAGES[@]}"; do
    if ! python -c "import $pkg" 2>/dev/null; then
        echo "Error: Python package $pkg is not installed."
        exit 1
    else
        echo "Python package $pkg is installed."
    fi
done

echo "Environment validation successful!"
exit 0

