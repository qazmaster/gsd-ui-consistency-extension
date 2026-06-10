#!/usr/bin/env python3
"""Test: No duplicate flags in workflow template"""

import os
import re
from pathlib import Path

_TEST_DIR = os.path.dirname(os.path.abspath(__file__))

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

# Try to find workflow template in multiple locations
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

WORKFLOW = _find_workflow()


def test_no_duplicate_classify_flag():
    """--classify flag must appear only once in <flags> section"""
    content = WORKFLOW.read_text()

    flags_section = re.search(r'<flags>(.*?)</flags>', content, re.DOTALL)
    assert flags_section, "Flags section not found"

    flags = flags_section.group(1)
    classify_count = len(re.findall(r'--classify', flags))

    assert classify_count == 1, \
        f"--classify flag appears {classify_count} times, expected 1"


if __name__ == "__main__":
    test_no_duplicate_classify_flag()
    print("✅ No duplicate flags test passes")
