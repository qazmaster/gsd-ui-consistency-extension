#!/usr/bin/env python3
"""Test: Extension package has correct directory structure and required files"""

import json
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


def test_package_json_exists():
    """package.json must exist"""
    assert (EXTENSION_DIR / "package.json").exists(), "package.json not found"


def test_extension_manifest_exists():
    """extension-manifest.json must exist"""
    assert (EXTENSION_DIR / "extension-manifest.json").exists(), "extension-manifest.json not found"


def test_index_ts_exists():
    """index.ts entry point must exist"""
    assert (EXTENSION_DIR / "index.ts").exists(), "index.ts not found"


def test_readme_exists():
    """README.md should exist for documentation"""
    assert (EXTENSION_DIR / "README.md").exists(), "README.md not found"


def test_skills_directory_exists():
    """skills/ directory with ui-consistency skill must exist"""
    # Check in extension dir first (source repo)
    skill_dir = EXTENSION_DIR / "skills" / "ui-consistency"
    # Fallback to installed location
    if not skill_dir.exists():
        skill_dir = Path.home() / ".agents" / "skills" / "ui-consistency"
    assert skill_dir.exists(), f"Skill directory not found: {skill_dir}"
    assert (skill_dir / "SKILL.md").exists(), "SKILL.md not found in skill directory"


def test_prompts_directory_exists():
    """prompts/ directory with workflow template must exist"""
    prompts_dir = EXTENSION_DIR / "prompts"
    assert prompts_dir.exists(), "prompts/ directory not found"
    assert (prompts_dir / "ui-consistency.md").exists(), "ui-consistency.md workflow template not found"


def test_workflows_directory_exists():
    """skills/ui-consistency/workflows/ must contain workflow files"""
    workflows_dir = EXTENSION_DIR / "skills" / "ui-consistency" / "workflows"
    # Fallback to installed location
    if not workflows_dir.exists():
        workflows_dir = Path.home() / ".agents" / "skills" / "ui-consistency" / "workflows"
    assert workflows_dir.exists(), "workflows/ directory not found"
    
    required_workflows = [
        "generate-design-system.md",
        "audit-and-fix.md",
        "quick-scan.md",
        "fix-only.md",
    ]
    for wf in required_workflows:
        assert (workflows_dir / wf).exists(), f"Workflow file not found: {wf}"


def test_references_directory_exists():
    """skills/ui-consistency/references/ must contain reference docs"""
    refs_dir = EXTENSION_DIR / "skills" / "ui-consistency" / "references"
    # Fallback to installed location
    if not refs_dir.exists():
        refs_dir = Path.home() / ".agents" / "skills" / "ui-consistency" / "references"
    assert refs_dir.exists(), "references/ directory not found"
    
    required_refs = [
        "complexity-detection.md",
        "design-system-format.md",
        "legacy-classification.md",
        "token-inheritance.md",
        "wave-planning.md",
    ]
    for ref in required_refs:
        assert (refs_dir / ref).exists(), f"Reference file not found: {ref}"


def test_tests_directory_exists():
    """skills/ui-consistency/tests/ must contain test files"""
    tests_dir = EXTENSION_DIR / "skills" / "ui-consistency" / "tests"
    # Fallback to installed location
    if not tests_dir.exists():
        tests_dir = Path.home() / ".agents" / "skills" / "ui-consistency" / "tests"
    assert tests_dir.exists(), "tests/ directory not found"
    assert (tests_dir / "run_all_tests.py").exists(), "run_all_tests.py not found"


if __name__ == "__main__":
    test_package_json_exists()
    test_extension_manifest_exists()
    test_index_ts_exists()
    test_readme_exists()
    test_skills_directory_exists()
    test_prompts_directory_exists()
    test_workflows_directory_exists()
    test_references_directory_exists()
    test_tests_directory_exists()
    print("✅ All extension package structure tests pass")
