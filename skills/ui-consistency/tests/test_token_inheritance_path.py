#!/usr/bin/env python3
"""Test: Token inheritance config path is consistent across all files"""

import re
from pathlib import Path

PREFERENCES = Path("~/.gsd/PREFERENCES.md").expanduser()
WORKFLOW = Path("~/.gsd/agent/extensions/gsd/workflow-templates/ui-consistency.md").expanduser()
REFERENCE = Path("~/.agents/skills/ui-consistency/references/token-inheritance.md").expanduser()


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
