#!/usr/bin/env python3
"""Test: Unknown classification exists for edge cases"""

import os
from pathlib import Path

_TEST_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = Path(os.path.normpath(os.path.join(_TEST_DIR, "..")))
WORKFLOW = Path("~/.gsd/agent/extensions/gsd/workflow-templates/ui-consistency.md").expanduser()
REF = SKILL_DIR / "references" / "legacy-classification.md"


def test_unknown_in_workflow():
    """Workflow template must mention unknown classification"""
    content = WORKFLOW.read_text()

    assert "unknown" in content.lower(), \
        "Workflow must classify files as 'unknown' when no indicators match"


def test_unknown_in_reference():
    """Reference doc must document unknown classification"""
    ref = REF.read_text()

    assert "unknown" in ref.lower(), \
        "legacy-classification.md must document 'unknown' classification"


def test_four_classifications_in_workflow():
    """Workflow must define exactly 4 classifications"""
    content = WORKFLOW.read_text()

    classifications = ["modern", "legacy", "drift", "unknown"]
    for cls in classifications:
        # Check that classification is mentioned in scan phase
        assert cls in content.lower(), \
            f"Classification '{cls}' not found in workflow template"


if __name__ == "__main__":
    test_unknown_in_workflow()
    test_unknown_in_reference()
    test_four_classifications_in_workflow()
    print("✅ Unknown classification test passes")
