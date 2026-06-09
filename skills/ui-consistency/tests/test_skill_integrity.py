#!/usr/bin/env python3
"""Test: Skill files (SKILL.md, workflows, references) are complete and consistent"""

import re
from pathlib import Path

EXTENSION_DIR = Path("~/.pi/agent/extensions/ui-consistency").expanduser()
SKILL_DIR = EXTENSION_DIR / "skills" / "ui-consistency"


def test_skill_md_exists():
    """SKILL.md must exist"""
    assert (SKILL_DIR / "SKILL.md").exists(), "SKILL.md not found"


def test_skill_md_has_name():
    """SKILL.md must have name: ui-consistency"""
    content = (SKILL_DIR / "SKILL.md").read_text()
    assert "name: ui-consistency" in content, "Missing or incorrect name in SKILL.md"


def test_skill_md_has_objective():
    """SKILL.md must have objective section"""
    content = (SKILL_DIR / "SKILL.md").read_text()
    assert "<objective>" in content, "Missing <objective> section"


def test_skill_md_has_routing():
    """SKILL.md must have routing section"""
    content = (SKILL_DIR / "SKILL.md").read_text()
    assert "<routing>" in content, "Missing <routing> section"


def test_skill_md_has_workflows_index():
    """SKILL.md must reference all 4 workflows"""
    content = (SKILL_DIR / "SKILL.md").read_text()
    
    required_workflows = [
        "generate-design-system.md",
        "audit-and-fix.md",
        "quick-scan.md",
        "fix-only.md",
    ]
    
    for wf in required_workflows:
        assert wf in content, f"Missing workflow reference: {wf}"


def test_skill_md_has_references_index():
    """SKILL.md must reference all 5 reference docs"""
    content = (SKILL_DIR / "SKILL.md").read_text()
    
    required_refs = [
        "complexity-detection.md",
        "design-system-format.md",
        "legacy-classification.md",
        "token-inheritance.md",
        "wave-planning.md",
    ]
    
    for ref in required_refs:
        assert ref in content, f"Missing reference: {ref}"


def test_skill_md_has_auto_mode_integration():
    """SKILL.md must document auto-mode integration"""
    content = (SKILL_DIR / "SKILL.md").read_text()
    assert "<auto_mode_integration>" in content, "Missing <auto_mode_integration> section"


def test_skill_md_documents_implemented_layers():
    """SKILL.md must document which layers are implemented"""
    content = (SKILL_DIR / "SKILL.md").read_text()
    assert "Implemented layers:" in content, "Missing implemented layers documentation"
    assert "NOT implemented" in content, "Missing NOT implemented documentation"


def test_workflows_have_consistent_structure():
    """All workflow files must have consistent markdown structure"""
    workflows_dir = SKILL_DIR / "workflows"
    
    for wf_file in workflows_dir.glob("*.md"):
        content = wf_file.read_text()
        
        # Must have purpose or description
        assert "## " in content or "# " in content, f"{wf_file.name}: Missing headers"
        
        # Must have process or step structure (numbered lists count)
        has_structure = (
            "Phase" in content or 
            "Step" in content or 
            "## " in content or
            "process" in content.lower() or
            re.search(r'^\d+\.', content, re.MULTILINE) is not None
        )
        assert has_structure, f"{wf_file.name}: Missing process/step structure"


def test_references_have_required_sections():
    """Reference docs must have required content"""
    refs_dir = SKILL_DIR / "references"
    
    # complexity-detection.md
    complexity = (refs_dir / "complexity-detection.md").read_text()
    assert "simple" in complexity.lower(), "complexity-detection.md must mention simple mode"
    assert "medium" in complexity.lower(), "complexity-detection.md must mention medium mode"
    assert "hard" in complexity.lower(), "complexity-detection.md must mention hard mode"
    
    # design-system-format.md
    ds_format = (refs_dir / "design-system-format.md").read_text()
    assert "STYLE_PICK" in ds_format, "design-system-format.md must mention STYLE_PICK"
    assert "DESIGN_DNA" in ds_format, "design-system-format.md must mention DESIGN_DNA"
    
    # legacy-classification.md
    legacy = (refs_dir / "legacy-classification.md").read_text()
    assert "modern" in legacy.lower(), "legacy-classification.md must mention modern"
    assert "legacy" in legacy.lower(), "legacy-classification.md must mention legacy"
    assert "drift" in legacy.lower(), "legacy-classification.md must mention drift"


def test_skill_md_has_success_criteria():
    """SKILL.md must have success criteria"""
    content = (SKILL_DIR / "SKILL.md").read_text()
    assert "<success_criteria>" in content, "Missing <success_criteria> section"


def test_skill_md_has_quick_start():
    """SKILL.md must have quick start guide"""
    content = (SKILL_DIR / "SKILL.md").read_text()
    assert "<quick_start>" in content, "Missing <quick_start> section"


if __name__ == "__main__":
    test_skill_md_exists()
    test_skill_md_has_name()
    test_skill_md_has_objective()
    test_skill_md_has_routing()
    test_skill_md_has_workflows_index()
    test_skill_md_has_references_index()
    test_skill_md_has_auto_mode_integration()
    test_skill_md_documents_implemented_layers()
    test_workflows_have_consistent_structure()
    test_references_have_required_sections()
    test_skill_md_has_success_criteria()
    test_skill_md_has_quick_start()
    print("✅ All skill integrity tests pass")
