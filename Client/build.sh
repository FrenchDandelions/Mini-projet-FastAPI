#!/bin/bash

set -e

APP_NAME="myapp"
MAIN_FILE="main.py"
TARGET_DIR="$HOME/.local/bin"
ARCH=$(uname -s)

python -m venv .venv

# Activate virtual environment
if [[ "$ARCH" == "Linux" || "$ARCH" == "Darwin" ]]; then
    source "./.venv/bin/activate"
elif [[ "$ARCH" =~ "MINGW" || "$ARCH" =~ "MSYS" || "$ARCH" =~ "CYGWIN" ]]; then
    source "./.venv/Scripts/activate"
else
    echo "Unsupported OS: $ARCH"
    exit 1
fi

# Ensure pyinstaller is installed
pip install -r requirements.txt

# Build standalone
pyinstaller --onefile --name "$APP_NAME" "$MAIN_FILE"

# Copy to local bin
mkdir -p "$TARGET_DIR"
cp "dist/$APP_NAME" "$TARGET_DIR/$APP_NAME"

# PATH check
if [[ ":$PATH:" != *":$TARGET_DIR:"* ]]; then
    echo "⚠️ $TARGET_DIR is not in your PATH."
    echo "👉 Add this to your shell config:"
    echo "export PATH=\"$TARGET_DIR:\$PATH\""
fi

# Clean
rm -rf build dist __pycache__ "$APP_NAME.spec"

# Done
echo "✅ Installed $APP_NAME to $TARGET_DIR"
echo "You can now run: $APP_NAME"
