#!/usr/bin/env bash
set -euo pipefail

# UI Consistency Extension Installer
# Usage: ./install.sh [target_dir]
# Default target: ~/.pi/agent/extensions/ui-consistency

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${1:-$HOME/.pi/agent/extensions/ui-consistency}"

echo "Installing UI Consistency Extension..."
echo "Source: $SCRIPT_DIR"
echo "Target: $TARGET_DIR"

# Create target directory
mkdir -p "$TARGET_DIR"

# Copy all files
cp -r "$SCRIPT_DIR/"* "$TARGET_DIR/"

# Remove install script from target (self-cleanup)
rm -f "$TARGET_DIR/install.sh"

# Run validation tests (skip if SKIP_TESTS is set to avoid recursion)
echo ""
if [ "${SKIP_TESTS:-}" = "1" ]; then
    echo "Skipping validation tests (SKIP_TESTS=1)"
else
    echo "Running validation tests..."
    TEST_DIR="$TARGET_DIR/skills/ui-consistency/tests"
    if [ -f "$TEST_DIR/run_all_tests.py" ]; then
        if python3 "$TEST_DIR/run_all_tests.py"; then
            echo ""
            echo "✓ All validation tests passed"
        else
            echo ""
            echo "⚠️  Some validation tests failed — check output above"
            exit 1
        fi
    else
        echo "⚠️  Test runner not found — skipping validation"
    fi
fi

echo ""
echo "✓ UI Consistency Extension installed to $TARGET_DIR"
echo ""
echo "Next steps:"
echo "  1. Run GSD with the extension:"
echo "     gsd -e $TARGET_DIR"
echo ""
echo "  2. Or reload GSD if already running:"
echo "     /reload"
echo ""
echo "  3. Use commands:"
echo "     /ui-consistency scan [path]"
echo "     /ui-consistency audit [path]"
echo "     /ui-consistency generate"
echo "     /ui-consistency fix <file>"
echo ""
echo "  4. Or start the workflow:"
echo "     /gsd start ui-consistency"
