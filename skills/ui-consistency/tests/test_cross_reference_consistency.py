#!/usr/bin/env python3
"""Test: Cross-references between skill, workflow, and extension are consistent"""

import os
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
    # Fallback: check if we're installed and look in ~/.gsd/
    gsd_ext = Path.home() / ".gsd" / "agent" / "extensions" / "ui-consistency"
    if (gsd_ext / marker).exists():
        return str(gsd_ext)
    return os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))

_EXTENSION_ROOT = _find_root()
EXTENSION_DIR = Path(_EXTENSION_ROOT)
SKILL_DIR = EXTENSION_DIR / "skills" / "ui-consistency"


def test_skill_references_extension_tools():
    """SKILL.md should reference tools that exist in index.ts"""
    skill = (SKILL_DIR / "SKILL.md").read_text()
    index = (EXTENSION_DIR / "index.ts").read_text()
    
    # Check that tools mentioned in skill exist in extension
    tool_names = [
        "ui_consistency_scan",
        "ui_consistency_audit",
        "ui_consistency_generate_design_system",
    ]
    
    for tool in tool_names:
        if tool in skill:
            assert f'name: "{tool}"' in index, f"Tool {tool} referenced in SKILL.md but not registered in index.ts"


def test_workflow_references_same_phases_as_skill():
    """Workflow files phases should match skill documentation"""
    # Check primary workflows (not deprecated template)
    workflow_files = [
        SKILL_DIR / "workflows" / "generate-design-system.md",
        SKILL_DIR / "workflows" / "audit-and-fix.md",
        SKILL_DIR / "workflows" / "quick-scan.md",
    ]
    
    skill = (SKILL_DIR / "SKILL.md").read_text()
    
    # All workflows + skill should mention all 6 phases
    phases = ["research", "generate", "scan", "audit", "fix", "verify"]
    for phase in phases:
        assert phase in skill.lower(), f"Phase {phase} missing from skill"
        
    # At least one workflow should mention each phase
    for phase in phases:
        found_in_any = any(phase in wf.read_text().lower() for wf in workflow_files if wf.exists())
        assert found_in_any, f"Phase {phase} missing from all workflow files"


def test_skill_and_workflow_agree_on_artifacts():
    """SKILL.md and workflow should agree on artifact locations"""
    workflow = (EXTENSION_DIR / "prompts" / "ui-consistency.md").read_text()
    skill = (SKILL_DIR / "SKILL.md").read_text()
    
    # Both should reference .gsd/ui-gates/
    assert ".gsd/ui-gates/" in workflow, "Workflow missing .gsd/ui-gates/ reference"
    assert ".gsd/ui-gates/" in skill, "Skill missing .gsd/ui-gates/ reference"


def test_extension_manifest_matches_index_ts():
    """extension-manifest.json tools must match index.ts registrations"""
    import json
    
    manifest = json.loads((EXTENSION_DIR / "extension-manifest.json").read_text())
    index = (EXTENSION_DIR / "index.ts").read_text()
    
    manifest_tools = set(manifest["provides"]["tools"])
    
    # Extract tool names from index.ts
    import re
    index_tools = set(re.findall(r'name:\s*"(ui_consistency_\w+)"', index))
    
    assert manifest_tools == index_tools, f"Tool mismatch: manifest={manifest_tools}, index={index_tools}"


def test_extension_manifest_matches_package_json():
    """extension-manifest.json id should match package.json name"""
    import json
    
    manifest = json.loads((EXTENSION_DIR / "extension-manifest.json").read_text())
    package = json.loads((EXTENSION_DIR / "package.json").read_text())
    
    assert manifest["id"] == "ui-consistency", "Manifest id should be ui-consistency"
    assert "ui-consistency" in package["name"], "Package name should contain ui-consistency"


def test_workflow_flags_match_skill_documentation():
    """Workflow flags should match skill quick_start flags"""
    workflow = (EXTENSION_DIR / "prompts" / "ui-consistency.md").read_text()
    skill = (SKILL_DIR / "SKILL.md").read_text()
    
    # Check common flags
    flags = ["--audit-only", "--fix", "--fix-tokens", "--classify"]
    for flag in flags:
        if flag in workflow:
            assert flag in skill, f"Flag {flag} in workflow but not in skill docs"


def test_complexity_modes_consistent():
    """Complexity modes should be consistent across all files"""
    workflow = (EXTENSION_DIR / "prompts" / "ui-consistency.md").read_text()
    skill = (SKILL_DIR / "SKILL.md").read_text()
    complexity = (SKILL_DIR / "references" / "complexity-detection.md").read_text()
    
    modes = ["simple", "medium", "hard"]
    for mode in modes:
        assert mode in workflow.lower(), f"Mode {mode} missing from workflow"
        assert mode in skill.lower(), f"Mode {mode} missing from skill"
        assert mode in complexity.lower(), f"Mode {mode} missing from complexity-detection"


def test_design_system_files_consistent():
    """All files should reference same design system filenames"""
    workflow = (EXTENSION_DIR / "prompts" / "ui-consistency.md").read_text()
    skill = (SKILL_DIR / "SKILL.md").read_text()
    index = (EXTENSION_DIR / "index.ts").read_text()
    
    ds_files = ["STYLE_PICK.md", "DESIGN_DNA.md", "COMPONENT_PLAN.md"]
    for ds_file in ds_files:
        assert ds_file in workflow, f"{ds_file} missing from workflow"
        assert ds_file in skill, f"{ds_file} missing from skill"
        assert ds_file in index, f"{ds_file} missing from index.ts"


if __name__ == "__main__":
    test_skill_references_extension_tools()
    test_workflow_references_same_phases_as_skill()
    test_skill_and_workflow_agree_on_artifacts()
    test_extension_manifest_matches_index_ts()
    test_extension_manifest_matches_package_json()
    test_workflow_flags_match_skill_documentation()
    test_complexity_modes_consistent()
    test_design_system_files_consistent()
    print("✅ All cross-reference consistency tests pass")
