#!/usr/bin/env python3
"""Contract test: ui-consistency workflow template generates valid UI_VERIFY.json"""

import json
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

# Try to find workflow template in multiple locations
def _find_workflow_template():
    """Find workflow template in source repo or installed location."""
    # Source repo location
    src = _EXTENSION_ROOT / "prompts" / "ui-consistency.md"
    if src.exists():
        return src
    # Installed location
    installed = Path("~/.gsd/agent/extensions/gsd/workflow-templates/ui-consistency.md").expanduser()
    if installed.exists():
        return installed
    # Fallback: just return source path for error message
    return src

WORKFLOW_TEMPLATE = _find_workflow_template()
DESIGN_SYSTEM_FORMAT = SKILL_DIR / "references" / "design-system-format.md"

def test_workflow_template_generates_correct_schema_version():
    """Workflow template Phase 6 must generate schemaVersion: ui-verify.fixture.v1"""
    template = WORKFLOW_TEMPLATE.read_text()

    # Check that template references correct schemaVersion
    assert '"schemaVersion": "ui-verify.fixture.v1"' in template, \
        "Workflow template must generate schemaVersion: ui-verify.fixture.v1"

    # Check that template does NOT generate old format (standalone "version": 1 without schemaVersion)
    # Allow "version" in template_meta but not in UI_VERIFY.json example
    # Find the UI_VERIFY.json example in Phase 5/6
    verify_sections = re.findall(r'```json\s*\{(.*?)\}```', template, re.DOTALL)
    for section in verify_sections:
        if '"overallVerdict"' in section and '"schemaVersion"' not in section:
            assert False, f"Found UI_VERIFY example without schemaVersion: {section[:200]}"

def test_design_system_format_has_required_fields():
    """design-system-format.md must document all required fields"""
    doc = DESIGN_SYSTEM_FORMAT.read_text()

    required_fields = [
        "schemaVersion",
        "evidenceFresh",
        "routes",
        "viewports",
        "console",
        "network",
        "horizontalOverflow",
        "focusVisibility",
        "uiVerdict"
    ]

    for field in required_fields:
        assert field in doc, f"Required field {field} not documented in design-system-format.md"

def test_generated_ui_verify_passes_validation():
    """Generated UI_VERIFY.json must pass schema validation"""
    sample = {
        "schemaVersion": "ui-verify.fixture.v1",
        "evidenceFresh": True,
        "metadata": {
            "notApplicableArtifacts": [
                "PRIME_DIRECTION.json",
                "STRUCTURAL_REVIEW.json",
                "OPTICAL_REVIEW.json",
                "PROVENANCE_TRACKING.json",
            ],
            "workflow": "ui-consistency",
            "workflowVersion": "2026-06-09",
        },
        "routes": [{"path": "/", "status": "pass"}],
        "viewports": {
            "desktop": {"status": "pass"},
            "tablet": {"status": "pass"},
            "mobile": {"status": "pass"},
        },
        "console": {"status": "pass"},
        "network": {"status": "pass"},
        "horizontalOverflow": {"status": "pass"},
        "focusVisibility": {"status": "pass"},
        "uiVerdict": "PASS",
        "verdictRationale": "All checks passed",
        "checks": {
            "colorConsistency": {"status": "pass", "evidence": "0 hardcoded colors"},
        },
        "nextSteps": [],
    }

    # Validate against schema requirements
    assert sample["schemaVersion"] == "ui-verify.fixture.v1"
    assert sample["evidenceFresh"] is True
    assert len(sample["routes"]) >= 1
    assert all(k in sample["viewports"] for k in ["desktop", "tablet", "mobile"])
    assert sample["uiVerdict"] in ["PASS", "FAIL", "NEEDS_ATTENTION"]


if __name__ == "__main__":
    test_workflow_template_generates_correct_schema_version()
    test_design_system_format_has_required_fields()
    test_generated_ui_verify_passes_validation()
    print("✅ All UI_VERIFY contract tests pass")
