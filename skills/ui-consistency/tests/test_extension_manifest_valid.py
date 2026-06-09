#!/usr/bin/env python3
"""Test: extension-manifest.json is valid and complete"""

import json
from pathlib import Path

EXTENSION_DIR = Path("~/.pi/agent/extensions/ui-consistency").expanduser()
MANIFEST = EXTENSION_DIR / "extension-manifest.json"


def test_manifest_is_valid_json():
    """extension-manifest.json must be valid JSON"""
    manifest = json.loads(MANIFEST.read_text())
    assert isinstance(manifest, dict), "Manifest must be a JSON object"


def test_manifest_has_required_fields():
    """Manifest must have id, name, version, description, tier, requires, provides"""
    manifest = json.loads(MANIFEST.read_text())
    
    required_fields = ["id", "name", "version", "description", "tier", "requires", "provides"]
    for field in required_fields:
        assert field in manifest, f"Missing required field: {field}"


def test_manifest_id_is_valid():
    """id must be 'ui-consistency'"""
    manifest = json.loads(MANIFEST.read_text())
    assert manifest["id"] == "ui-consistency", f"Expected id 'ui-consistency', got '{manifest['id']}'"


def test_manifest_tier_is_community():
    """tier should be 'community' for user extensions"""
    manifest = json.loads(MANIFEST.read_text())
    assert manifest["tier"] == "community", f"Expected tier 'community', got '{manifest['tier']}'"


def test_manifest_provides_tools():
    """provides.tools must list all 4 tools"""
    manifest = json.loads(MANIFEST.read_text())
    tools = manifest["provides"]["tools"]
    
    expected_tools = [
        "ui_consistency_scan",
        "ui_consistency_audit",
        "ui_consistency_generate_design_system",
        "ui_consistency_fix",
        "ui_consistency_self_test",
    ]
    
    for tool in expected_tools:
        assert tool in tools, f"Missing tool in manifest: {tool}"
    
    assert len(tools) == 5, f"Expected 5 tools, got {len(tools)}"


def test_manifest_provides_commands():
    """provides.commands must include 'ui-consistency'"""
    manifest = json.loads(MANIFEST.read_text())
    commands = manifest["provides"]["commands"]
    assert "ui-consistency" in commands, "Missing command 'ui-consistency'"


def test_manifest_provides_hooks():
    """provides.hooks must include session_start and before_agent_start"""
    manifest = json.loads(MANIFEST.read_text())
    hooks = manifest["provides"]["hooks"]
    
    assert "session_start" in hooks, "Missing hook 'session_start'"
    assert "before_agent_start" in hooks, "Missing hook 'before_agent_start'"


def test_manifest_version_is_semver():
    """version must follow semver format"""
    manifest = json.loads(MANIFEST.read_text())
    version = manifest["version"]
    parts = version.split(".")
    assert len(parts) == 3, f"Version must be semver (x.y.z), got: {version}"
    assert all(p.isdigit() for p in parts), f"Version parts must be numeric, got: {version}"


def test_manifest_platform_requirement():
    """requires.platform must be specified"""
    manifest = json.loads(MANIFEST.read_text())
    assert "platform" in manifest["requires"], "Missing platform requirement"
    assert manifest["requires"]["platform"].startswith(">="), "Platform should have minimum version"


if __name__ == "__main__":
    test_manifest_is_valid_json()
    test_manifest_has_required_fields()
    test_manifest_id_is_valid()
    test_manifest_tier_is_community()
    test_manifest_provides_tools()
    test_manifest_provides_commands()
    test_manifest_provides_hooks()
    test_manifest_version_is_semver()
    test_manifest_platform_requirement()
    print("✅ All extension manifest validation tests pass")
