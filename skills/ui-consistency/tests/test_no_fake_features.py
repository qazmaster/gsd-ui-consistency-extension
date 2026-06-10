#!/usr/bin/env python3
"""Test: No fake/unimplemented features in config"""

import os
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
    # Fallback: assume we're in source repo
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

PREFERENCES = _find_preferences()
SKILL = SKILL_DIR / "SKILL.md"


def test_no_prompt_context_injection():
    """promptContext.injection must not exist at top-level - feature not implemented"""
    content = PREFERENCES.read_text()

    # Check that there's no standalone uiGates section with injection
    # uiGates is acceptable if it's only for the project-local extension config
    # but promptContext.injection is not a real preference key
    assert "injection: enabled" not in content, \
        "promptContext.injection is not implemented as a global pref - remove from config"


def test_no_standalone_uigates_section():
    """uiGates top-level section must not exist - move to uiConsistency"""
    content = PREFERENCES.read_text()

    assert "uiGates:" not in content, \
        "uiGates top-level section should be replaced with uiConsistency"


def test_no_completion_enforcement_fake():
    """completionEnforcement must not exist as top-level pref"""
    content = PREFERENCES.read_text()

    # completionEnforcement is a project-local extension config, not a global pref
    assert "completionEnforcement:" not in content, \
        "completionEnforcement is not a global pref - belongs to project-local extension"


def test_only_working_config_present():
    """Only working config sections should exist"""
    content = PREFERENCES.read_text()

    # uiConsistency should exist
    assert "uiConsistency:" in content, "uiConsistency section should exist"

    # pre_dispatch_hooks should still work
    assert "pre_dispatch_hooks:" in content, "pre_dispatch_hooks should exist"


if __name__ == "__main__":
    test_no_prompt_context_injection()
    test_no_standalone_uigates_section()
    test_no_completion_enforcement_fake()
    test_only_working_config_present()
    print("✅ All no-fake-features tests pass")
