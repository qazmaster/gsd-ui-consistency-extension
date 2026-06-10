#!/usr/bin/env python3
"""Test: workflow template (prompts/ui-consistency.md) is valid and complete"""

import os
import re
from pathlib import Path

def _find_root(marker="index.ts", max_depth=5):
    """Walk up from this file to find directory containing marker."""
    d = os.path.dirname(os.path.abspath(__file__))
    for _ in range(max_depth):
        if os.path.isfile(os.path.join(d, marker)):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))

_EXTENSION_ROOT = _find_root()
EXTENSION_DIR = Path(_EXTENSION_ROOT)
WORKFLOW_TEMPLATE = EXTENSION_DIR / "prompts" / "ui-consistency.md"


def test_workflow_template_exists():
    """ui-consistency.md must exist in prompts/"""
    assert WORKFLOW_TEMPLATE.exists(), "Workflow template not found"


def test_workflow_has_template_meta():
    """Workflow must have <template_meta> block"""
    content = WORKFLOW_TEMPLATE.read_text()
    assert "<template_meta>" in content, "Missing <template_meta> block"
    assert "</template_meta>" in content, "Missing </template_meta> closing tag"


def test_workflow_has_name():
    """template_meta must have name: ui-consistency"""
    content = WORKFLOW_TEMPLATE.read_text()
    meta_match = re.search(r'<template_meta>(.*?)</template_meta>', content, re.DOTALL)
    assert meta_match, "Could not extract template_meta"
    meta = meta_match.group(1)
    assert "name: ui-consistency" in meta, "Missing or incorrect name in template_meta"


def test_workflow_has_mode():
    """template_meta must have mode: markdown-phase"""
    content = WORKFLOW_TEMPLATE.read_text()
    meta_match = re.search(r'<template_meta>(.*?)</template_meta>', content, re.DOTALL)
    meta = meta_match.group(1)
    assert "mode: markdown-phase" in meta, "Missing or incorrect mode in template_meta"


def test_workflow_has_phases():
    """Workflow must define 6 phases (0-5)"""
    content = WORKFLOW_TEMPLATE.read_text()
    
    phase_headers = re.findall(r'## Phase \d+:', content)
    assert len(phase_headers) == 6, f"Expected 6 phases, found {len(phase_headers)}"


def test_workflow_has_all_six_phases():
    """Workflow must have all 6 phases: research, generate, scan, audit, fix, verify"""
    content = WORKFLOW_TEMPLATE.read_text()
    
    required_phases = ["research", "generate", "scan", "audit", "fix", "verify"]
    for phase in required_phases:
        assert f"## Phase" in content and phase in content.lower(), f"Missing phase: {phase}"


def test_workflow_has_flags():
    """Workflow must document flags"""
    content = WORKFLOW_TEMPLATE.read_text()
    assert "<flags>" in content or "--audit-only" in content, "Missing flags documentation"


def test_workflow_has_outputs():
    """Workflow must document outputs/artifacts"""
    content = WORKFLOW_TEMPLATE.read_text()
    assert "<outputs>" in content or "## Artifacts" in content or "| Phase |" in content, "Missing outputs documentation"


def test_workflow_has_ui_verify_schema():
    """Workflow must reference correct UI_VERIFY.json schema"""
    content = WORKFLOW_TEMPLATE.read_text()
    assert '"schemaVersion": "ui-verify.fixture.v1"' in content, "Missing correct UI_VERIFY schema version"


def test_workflow_has_single_approval_gate():
    """Only Phase 1 should have approval gate"""
    content = WORKFLOW_TEMPLATE.read_text()
    
    gate_count = len(re.findall(r'^\d+\. \*\*Gate:\*\*', content, re.MULTILINE))
    assert gate_count == 1, f"Expected 1 approval gate, found {gate_count}"


def test_workflow_no_duplicate_flags():
    """No duplicate flag definitions in <flags> section"""
    content = WORKFLOW_TEMPLATE.read_text()
    
    # Extract only the <flags> section
    flags_match = re.search(r'<flags>(.*?)</flags>', content, re.DOTALL)
    if not flags_match:
        # If no <flags> section, skip this test
        return
    
    flags_section = flags_match.group(1)
    flags = re.findall(r'--([a-z-]+)', flags_section)
    flag_counts = {}
    for flag in flags:
        flag_counts[flag] = flag_counts.get(flag, 0) + 1
    
    duplicates = {k: v for k, v in flag_counts.items() if v > 1}
    assert not duplicates, f"Duplicate flags in <flags> section: {duplicates}"


def test_workflow_has_safety_section():
    """Workflow must have safety section"""
    content = WORKFLOW_TEMPLATE.read_text()
    assert "<safety>" in content or "## Safety" in content or "Hard mode" in content, "Missing safety documentation"


if __name__ == "__main__":
    test_workflow_template_exists()
    test_workflow_has_template_meta()
    test_workflow_has_name()
    test_workflow_has_mode()
    test_workflow_has_phases()
    test_workflow_has_all_six_phases()
    test_workflow_has_flags()
    test_workflow_has_outputs()
    test_workflow_has_ui_verify_schema()
    test_workflow_has_single_approval_gate()
    test_workflow_no_duplicate_flags()
    test_workflow_has_safety_section()
    print("✅ All workflow template validation tests pass")
