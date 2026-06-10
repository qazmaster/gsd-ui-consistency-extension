#!/usr/bin/env python3
"""Test: index.ts extension entry point has required registrations"""

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
INDEX_TS = EXTENSION_DIR / "index.ts"


def test_index_ts_exists():
    """index.ts must exist"""
    assert INDEX_TS.exists(), "index.ts not found"


def test_index_ts_has_default_export():
    """index.ts must export default function"""
    content = INDEX_TS.read_text()
    assert "export default function" in content, "Missing default export function"


def test_index_ts_registers_tools():
    """index.ts must register all 5 tools"""
    content = INDEX_TS.read_text()
    
    required_tools = [
        "ui_consistency_scan",
        "ui_consistency_audit",
        "ui_consistency_generate_design_system",
        "ui_consistency_fix",
        "ui_consistency_self_test",
    ]
    
    for tool in required_tools:
        assert f'name: "{tool}"' in content, f"Missing tool registration: {tool}"


def test_index_ts_registers_command():
    """index.ts must register /ui-consistency command"""
    content = INDEX_TS.read_text()
    assert 'pi.registerCommand("ui-consistency"' in content, "Missing command registration"


def test_index_ts_registers_hooks():
    """index.ts must register session_start and before_agent_start hooks"""
    content = INDEX_TS.read_text()
    assert 'pi.on("session_start"' in content, "Missing session_start hook"
    assert 'pi.on("before_agent_start"' in content, "Missing before_agent_start hook"


def test_index_ts_uses_string_enum():
    """index.ts must use StringEnum for string enums (not Type.Union)"""
    content = INDEX_TS.read_text()
    assert "StringEnum" in content, "Must use StringEnum for string enums"
    # Ensure no Type.Union or Type.Literal for enums
    union_pattern = re.compile(r'Type\.Union\s*\[')
    literal_pattern = re.compile(r'Type\.Literal\s*\(')
    assert not union_pattern.search(content), "Must not use Type.Union for enums"
    assert not literal_pattern.search(content), "Must not use Type.Literal for enums"


def test_index_ts_uses_typebox():
    """index.ts must import and use @sinclair/typebox"""
    content = INDEX_TS.read_text()
    assert 'from "@sinclair/typebox"' in content, "Missing @sinclair/typebox import"
    assert "Type.Object" in content, "Must use Type.Object for parameters"


def test_index_ts_checks_signal_aborted():
    """index.ts tools must check signal?.aborted"""
    content = INDEX_TS.read_text()
    assert "signal?.aborted" in content, "Must check signal?.aborted in tools"


def test_index_ts_has_design_system_constants():
    """index.ts must define DESIGN_SYSTEM_DIR constant"""
    content = INDEX_TS.read_text()
    assert 'const DESIGN_SYSTEM_DIR = ".gsd/ui-gates"' in content, "Missing DESIGN_SYSTEM_DIR constant"


def test_index_ts_has_has_design_system_helper():
    """index.ts must have hasDesignSystem helper"""
    content = INDEX_TS.read_text()
    assert "function hasDesignSystem(" in content, "Missing hasDesignSystem helper"


if __name__ == "__main__":
    test_index_ts_exists()
    test_index_ts_has_default_export()
    test_index_ts_registers_tools()
    test_index_ts_registers_command()
    test_index_ts_registers_hooks()
    test_index_ts_uses_string_enum()
    test_index_ts_uses_typebox()
    test_index_ts_checks_signal_aborted()
    test_index_ts_has_design_system_constants()
    test_index_ts_has_has_design_system_helper()
    print("✅ All index.ts validation tests pass")
