#!/usr/bin/env python3
"""Test: Only one approval gate in workflow (after Generate phase)"""

import re
from pathlib import Path

WORKFLOW = Path("~/.gsd/agent/extensions/gsd/workflow-templates/ui-consistency.md").expanduser()


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
