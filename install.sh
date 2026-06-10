#!/usr/bin/env bash
set -euo pipefail

# UI Consistency Extension Installer
# Usage: ./install.sh [target_dir]
# Default target: ~/.gsd/agent/extensions/ui-consistency

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${1:-$HOME/.gsd/agent/extensions/ui-consistency}"
SKILLS_TARGET_DIR="${HOME}/.agents/skills"

echo "Installing UI Consistency Extension..."
echo "Source: $SCRIPT_DIR"
echo "Target: $TARGET_DIR"
echo "Skills target: $SKILLS_TARGET_DIR"
echo ""

# ─── Step 1: Install extension files ────────────────────────────────────────

# Create target directory
mkdir -p "$TARGET_DIR"

# Copy extension files (excluding skills directory)
echo "[1/4] Installing extension files..."
for item in "$SCRIPT_DIR"/* "$SCRIPT_DIR"/.[^.]*; do
    # Skip if glob didn't match
    [ -e "$item" ] || continue
    basename="$(basename "$item")"
    # Skip skills directory — handled separately
    if [ "$basename" = "skills" ]; then
        continue
    fi
    cp -r "$item" "$TARGET_DIR/"
done

# Remove install script from target (self-cleanup)
rm -f "$TARGET_DIR/install.sh"

echo "  ✓ Extension files installed to $TARGET_DIR"

# ─── Step 2: Install skills to ~/.agents/skills/ ────────────────────────────

echo ""
echo "[2/4] Installing skills..."

# List of skills to install
SKILLS=("ui-consistency" "ui-ux-uat-gates")

for skill_name in "${SKILLS[@]}"; do
    skill_source="$SCRIPT_DIR/skills/$skill_name"
    skill_target="$SKILLS_TARGET_DIR/$skill_name"

    if [ ! -d "$skill_source" ]; then
        echo "  ⚠️  Skill source not found: $skill_source (skipping)"
        continue
    fi

    # Backup existing skill if present
    if [ -d "$skill_target" ]; then
        backup_dir="${skill_target}.bak.$(date +%s)"
        echo "  Backing up existing $skill_name to $backup_dir"
        mv "$skill_target" "$backup_dir"
    fi

    # Copy skill files
    mkdir -p "$skill_target"
    cp -r "$skill_source"/* "$skill_target/"

    # Remove Python cache files from target
    find "$skill_target" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find "$skill_target" -name "*.pyc" -delete 2>/dev/null || true

    echo "  ✓ Skill '$skill_name' installed to $skill_target"
done

# ─── Step 3: Verify required files ──────────────────────────────────────────

echo ""
echo "[3/4] Verifying installation..."

MISSING=0

# Check extension files
for file in "index.ts" "package.json" "extension-manifest.json"; do
    if [ ! -f "$TARGET_DIR/$file" ]; then
        echo "  ✗ Missing: $TARGET_DIR/$file"
        MISSING=$((MISSING + 1))
    fi
done

# Check skill files
for skill_name in "${SKILLS[@]}"; do
    if [ ! -f "$SKILLS_TARGET_DIR/$skill_name/SKILL.md" ]; then
        echo "  ✗ Missing: $SKILLS_TARGET_DIR/$skill_name/SKILL.md"
        MISSING=$((MISSING + 1))
    fi
done

# Check validator script
VALIDATOR="$SKILLS_TARGET_DIR/ui-ux-uat-gates/scripts/validate-ui-gate-pack.py"
if [ ! -f "$VALIDATOR" ]; then
    echo "  ✗ Missing validator: $VALIDATOR"
    MISSING=$((MISSING + 1))
fi

if [ $MISSING -gt 0 ]; then
    echo ""
    echo "⚠️  $MISSING required file(s) missing — installation may be incomplete"
    exit 1
fi

echo "  ✓ All required files present"

# ─── Step 4: Run validation tests ───────────────────────────────────────────

echo ""
echo "[4/4] Running validation tests..."

if [ "${SKIP_TESTS:-}" = "1" ]; then
    echo "  Skipping validation tests (SKIP_TESTS=1)"
else
    TEST_DIR="$SKILLS_TARGET_DIR/ui-consistency/tests"
    if [ -f "$TEST_DIR/run_all_tests.py" ]; then
        if python3 "$TEST_DIR/run_all_tests.py"; then
            echo ""
            echo "  ✓ All validation tests passed"
        else
            echo ""
            echo "  ⚠️  Some validation tests failed — check output above"
            exit 1
        fi
    else
        echo "  ⚠️  Test runner not found — skipping validation"
    fi
fi

# ─── Done ────────────────────────────────────────────────────────────────────

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "✓ UI Consistency Extension installed successfully"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "Installed components:"
echo "  • Extension:   $TARGET_DIR/"
echo "  • Skill:       $SKILLS_TARGET_DIR/ui-consistency/"
echo "  • Skill:       $SKILLS_TARGET_DIR/ui-ux-uat-gates/"
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
