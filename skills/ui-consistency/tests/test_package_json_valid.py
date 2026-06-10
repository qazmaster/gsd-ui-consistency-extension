#!/usr/bin/env python3
"""Test: package.json with pi manifest is valid and complete"""

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
    return os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))

_EXTENSION_ROOT = _find_root()
EXTENSION_DIR = Path(_EXTENSION_ROOT)
PACKAGE_JSON = EXTENSION_DIR / "package.json"


def test_package_json_is_valid_json():
    """package.json must be valid JSON"""
    pkg = json.loads(PACKAGE_JSON.read_text())
    assert isinstance(pkg, dict), "package.json must be a JSON object"


def test_package_has_name():
    """package.json must have name"""
    pkg = json.loads(PACKAGE_JSON.read_text())
    assert "name" in pkg, "Missing 'name' field"
    assert pkg["name"] == "pi-extension-ui-consistency", f"Unexpected name: {pkg['name']}"


def test_package_has_version():
    """package.json must have version"""
    pkg = json.loads(PACKAGE_JSON.read_text())
    assert "version" in pkg, "Missing 'version' field"


def test_package_has_keywords():
    """package.json must have pi-package keyword"""
    pkg = json.loads(PACKAGE_JSON.read_text())
    assert "keywords" in pkg, "Missing 'keywords' field"
    assert "pi-package" in pkg["keywords"], "Missing 'pi-package' keyword"


def test_package_has_pi_manifest():
    """package.json must have 'pi' manifest section"""
    pkg = json.loads(PACKAGE_JSON.read_text())
    assert "pi" in pkg, "Missing 'pi' manifest section"


def test_pi_manifest_has_extensions():
    """pi.extensions must point to entry point"""
    pkg = json.loads(PACKAGE_JSON.read_text())
    pi = pkg["pi"]
    assert "extensions" in pi, "Missing 'extensions' in pi manifest"
    assert "./index.ts" in pi["extensions"], "Missing './index.ts' in extensions"


def test_pi_manifest_has_skills():
    """pi.skills must point to skills directory"""
    pkg = json.loads(PACKAGE_JSON.read_text())
    pi = pkg["pi"]
    assert "skills" in pi, "Missing 'skills' in pi manifest"
    assert "./skills" in pi["skills"], "Missing './skills' in skills"


def test_pi_manifest_has_prompts():
    """pi.prompts must point to prompts directory"""
    pkg = json.loads(PACKAGE_JSON.read_text())
    pi = pkg["pi"]
    assert "prompts" in pi, "Missing 'prompts' in pi manifest"
    assert "./prompts" in pi["prompts"], "Missing './prompts' in prompts"


def test_package_has_peer_dependencies():
    """package.json must list required peer dependencies"""
    pkg = json.loads(PACKAGE_JSON.read_text())
    assert "peerDependencies" in pkg, "Missing 'peerDependencies'"
    
    required_peers = [
        "@gsd/pi-ai",
        "@gsd/pi-coding-agent",
        "@gsd/pi-tui",
        "@sinclair/typebox",
    ]
    
    for dep in required_peers:
        assert dep in pkg["peerDependencies"], f"Missing peer dependency: {dep}"
        assert pkg["peerDependencies"][dep] == "*", f"Peer dependency {dep} must be '*'"


def test_package_type_is_module():
    """package.json should have type: module for ES modules"""
    pkg = json.loads(PACKAGE_JSON.read_text())
    assert pkg.get("type") == "module", "Expected 'type': 'module' for ES modules"


if __name__ == "__main__":
    test_package_json_is_valid_json()
    test_package_has_name()
    test_package_has_version()
    test_package_has_keywords()
    test_package_has_pi_manifest()
    test_pi_manifest_has_extensions()
    test_pi_manifest_has_skills()
    test_pi_manifest_has_prompts()
    test_package_has_peer_dependencies()
    test_package_type_is_module()
    print("✅ All package.json validation tests pass")
