#!/usr/bin/env python3
"""Test: Only one approval gate in workflow (after Generate phase)"""

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
    # Fallback 1: check if we're in ~/.agents/skills/ and look for extension in ~/.gsd/
    gsd_ext = Path.home() / ".gsd" / "agent" / "extensions" / "gsd"
    if (gsd_ext / "index.ts").exists():
        return gsd_ext
    # Fallback 2: assume we're in source repo
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


def test_only_one_approval_gate():
    """Only Phase 1 (Generate) should have approval gate"""
    content = WORKFLOW.read_text()

    # Count explicit "Gate:" markers in phase sections
    gate_count = len(re.findall(r'^\d+\. \*\*Gate:\*\*', content, re.MULTILINE))

    assert gate_count == 1, \
        f"Found {gate_count} approval gates, expected 1 (after Generate phase only)"


def test_post_scan_is_recommendation_not_gate():
    """After Scan should be recommendation, not gate"""
    content = WORKFLOW.read_text()

    scan_section = re.search(r'## Phase 2: Scan.*?(?=## Phase 3:|$)', content, re.DOTALL)
    if scan_section:
        assert "**Gate:**" not in scan_section.group(), \
            "Phase 2 (Scan) should not have approval gate (use recommendation instead)"


def test_post_audit_is_recommendation_not_gate():
    """After Audit should be recommendation, not gate"""
    content = WORKFLOW.read_text()

    audit_section = re.search(r'## Phase 3: Audit.*?(?=## Phase 4:|$)', content, re.DOTALL)
    if audit_section:
        assert "**Gate:**" not in audit_section.group(), \
            "Phase 3 (Audit) should not have approval gate (use recommendation instead)"


if __name__ == "__main__":
    test_only_one_approval_gate()
    test_post_scan_is_recommendation_not_gate()
    test_post_audit_is_recommendation_not_gate()
    print("✅ Single approval gate test passes")
