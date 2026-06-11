#!/usr/bin/env bash
set -euo pipefail

# UI Consistency Unified Import Script
# Safely appends ui-consistency skill to existing GSD installation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_SKILLS_DIR="${1:-$HOME/.gsd/agent/skills/ui-consistency}"
TARGET_PREFERENCES="${2:-$HOME/.gsd/PREFERENCES.md}"

BACKUP_DIR="$HOME/.gsd/agent/skills/ui-consistency.bak.$(date +%s)"

echo "=== UI Consistency Unified Import ==="
echo "Source: $SCRIPT_DIR"
echo "Target skills: $TARGET_SKILLS_DIR"
echo "Target preferences: $TARGET_PREFERENCES"

# 1. Create backup
echo ""
echo "[1/5] Creating backup..."
if [ -d "$TARGET_SKILLS_DIR" ]; then
    cp -r "$TARGET_SKILLS_DIR" "$BACKUP_DIR"
    echo "Backup created: $BACKUP_DIR"
else
    echo "No existing skill to backup (fresh install)"
fi

# 2. Create directories
echo ""
echo "[2/5] Creating directories..."
mkdir -p "$TARGET_SKILLS_DIR/workflows"
mkdir -p "$TARGET_SKILLS_DIR/references"

# 3. Copy workflows
echo ""
echo "[3/5] Copying workflows..."
cp "$SCRIPT_DIR/workflows/"*.md "$TARGET_SKILLS_DIR/workflows/"
echo "Workflows copied:"
ls -1 "$TARGET_SKILLS_DIR/workflows/"

# 4. Copy references
echo ""
echo "[4/5] Copying references..."
cp "$SCRIPT_DIR/references/"*.md "$TARGET_SKILLS_DIR/references/"
echo "References copied:"
ls -1 "$TARGET_SKILLS_DIR/references/"

# 5. Append SKILL.md sections
echo ""
echo "[5/5] Appending SKILL.md sections..."
if [ -f "$TARGET_SKILLS_DIR/SKILL.md" ]; then
    # Check if already imported
    if grep -q "BEGIN UI CONSISTENCY UNIFIED APPEND" "$TARGET_SKILLS_DIR/SKILL.md"; then
        echo "WARNING: SKILL.md already contains unified sections. Skipping append."
        echo "To re-import, remove existing sections first."
    else
        cat "$SCRIPT_DIR/SKILL.md.patch" >> "$TARGET_SKILLS_DIR/SKILL.md"
        echo "SKILL.md sections appended."
    fi
else
    echo "ERROR: SKILL.md not found at $TARGET_SKILLS_DIR/SKILL.md"
    echo "Cannot append — stock GSD skill must exist first."
    exit 1
fi

# 6. Append PREFERENCES.md config (optional)
echo ""
echo "[6/6] Checking PREFERENCES.md..."
if [ -f "$TARGET_PREFERENCES" ]; then
    if grep -q "BEGIN UI CONSISTENCY CONFIG APPEND" "$TARGET_PREFERENCES"; then
        echo "WARNING: PREFERENCES.md already contains uiConsistency config. Skipping."
    else
        cat "$SCRIPT_DIR/config/PREFERENCES.md.patch" >> "$TARGET_PREFERENCES"
        echo "PREFERENCES.md config appended."
    fi
else
    echo "WARNING: PREFERENCES.md not found. Manual config required."
fi

echo ""
echo "=== Import Complete ==="
echo "Backup: $BACKUP_DIR"
echo ""
echo "Next steps:"
echo "1. Verify: skill_routing_health"
echo "2. Test: python3 $TARGET_SKILLS_DIR/tests/run_all_tests.py"
echo "3. If issues: restore from backup: cp -r $BACKUP_DIR $TARGET_SKILLS_DIR"
