#!/usr/bin/env python3
"""Test: Token inheritance config path is consistent across all files"""

import os
import re
from pathlib import Path

_TEST_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = Path(os.path.normpath(os.path.join(_TEST_DIR, "..")))

# Auto-detect extension root (walk up until we find index.ts)
def _find_extension_root():
    """Walk up from test dir to find extension root (where index.ts lives)."""
    current = Path(_TEST_DIR).resolve()
    while current != current.parent:
        if (current / "index.ts").exists():
            return current
        current = current.parent
    # Fallback 1: check if we're in ~/.agents/skills/ and look for extension in ~/.gsd/
    gsd_ext = Path.home() / ".gsd" / "agent" / "extensions" / "gsd"
    if (gsd_ext / "index.ts").exists():
        return gsd_ext
    # Fallback 2: assume we're in source repo
    return Path(_TEST_DIR).resolve().parents[2]

_EXTENSION_ROOT = _find_extension_root()

# Try to find PREFERENCES.md in multiple locations
def _find_preferences():
    """Find PREFERENCES.md in source repo or installed location."""
    # Source repo location
    src = _EXTENSION_ROOT / ".gsd" / "PREFERENCES.md"
    if src.exists():
        return src
    # Installed location
    installed = Path("~/.gsd/PREFERENCES.md").expanduser()
    if installed.exists():
        return installed
    # Fallback: just return source path for error message
    return src

def _find_workflow():
    """Find workflow template in source repo or installed location."""
    # Source repo location
    src = _EXTENSION_ROOT / "prompts" / "ui-consistency.md"
    if src.exists():
        return src
    # Installed location
    installed = Path("~/.gsd/agent/extensions/gsd/workflow-templates/ui-consistency.md").expanduser()
    if installed.exists():
        return installed
    # Fallback
    return src

PREFERENCES = _find_preferences()
WORKFLOW = _find_workflow()
REFERENCE = SKILL_DIR / "references" / "token-inheritance.md"


def test_preferences_has_design_system_base():
    """PREFERENCES.md must have designSystem.base at correct path"""
    content = PREFERENCES.read_text()

    # Must have designSystem accessible under uiConsistency
    assert "designSystem:" in content, "designSystem section missing"
    assert "base:" in content, "base field missing in designSystem"


def test_workflow_reads_correct_config_path():
    """Workflow template must reference uiConsistency.designSystem.base"""
    workflow = WORKFLOW.read_text()

    # Workflow must read uiConsistency.designSystem.base
    assert "uiConsistency.designSystem.base" in workflow, \
        "Workflow must read uiConsistency.designSystem.base, not designSystem.base"


def test_reference_doc_matches_config():
    """token-inheritance.md must document actual config structure"""
    ref = REFERENCE.read_text()
    prefs = PREFERENCES.read_text()

    # Determine actual nesting
    if "uiConsistency:" in prefs:
        # Check if designSystem is nested under uiConsistency
        section = re.search(r'uiConsistency:.*?(?=\n[a-zA-Z]|\Z)', prefs, re.DOTALL)
        if section and "designSystem:" in section.group():
            assert "uiConsistency.designSystem.base" in ref, \
                "Reference doc must document uiConsistency.designSystem.base path"


if __name__ == "__main__":
    test_preferences_has_design_system_base()
    test_workflow_reads_correct_config_path()
    test_reference_doc_matches_config()
    print("✅ All token inheritance path tests pass")
