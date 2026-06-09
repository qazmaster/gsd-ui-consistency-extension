#!/usr/bin/env python3
"""Test: install.sh script is valid and self-contained"""

import subprocess
import tempfile
from pathlib import Path

EXTENSION_DIR = Path("~/.pi/agent/extensions/ui-consistency").expanduser()
INSTALL_SCRIPT = EXTENSION_DIR / "install.sh"


def test_install_script_exists():
    """install.sh must exist"""
    assert INSTALL_SCRIPT.exists(), "install.sh not found"


def test_install_script_is_executable():
    """install.sh must be executable"""
    import stat
    mode = INSTALL_SCRIPT.stat().st_mode
    assert mode & stat.S_IXUSR, "install.sh must be executable"


def test_install_script_has_shebang():
    """install.sh must have bash shebang"""
    content = INSTALL_SCRIPT.read_text()
    assert content.startswith("#!/usr/bin/env bash"), "Missing bash shebang"


def test_install_script_has_set_euo():
    """install.sh must use set -euo pipefail"""
    content = INSTALL_SCRIPT.read_text()
    assert "set -euo pipefail" in content, "Missing 'set -euo pipefail'"


def test_install_script_creates_target_dir():
    """install.sh must create target directory"""
    content = INSTALL_SCRIPT.read_text()
    assert "mkdir -p" in content, "Missing mkdir -p for target directory"


def test_install_script_copies_files():
    """install.sh must copy files"""
    content = INSTALL_SCRIPT.read_text()
    assert "cp -r" in content, "Missing cp -r for file copy"


def test_install_script_self_cleanup():
    """install.sh must remove itself from target"""
    content = INSTALL_SCRIPT.read_text()
    assert 'rm -f "$TARGET_DIR/install.sh"' in content, "Missing self-cleanup"


def test_install_script_runs_successfully():
    """install.sh must run without errors (skip test runner to avoid recursion)"""
    with tempfile.TemporaryDirectory() as tmpdir:
        target = Path(tmpdir) / "ui-consistency"
        # Run install with SKIP_TESTS to avoid recursive test execution
        env = {"SKIP_TESTS": "1"}
        result = subprocess.run(
            ["bash", str(INSTALL_SCRIPT), str(target)],
            capture_output=True,
            text=True,
            env={**subprocess.os.environ, **env},
            timeout=30,
        )
        assert result.returncode == 0, f"install.sh failed: {result.stderr}"
        
        # Verify target was created
        assert target.exists(), "Target directory not created"
        
        # Verify key files exist
        assert (target / "package.json").exists(), "package.json not copied"
        assert (target / "extension-manifest.json").exists(), "extension-manifest.json not copied"
        assert (target / "index.ts").exists(), "index.ts not copied"
        
        # Verify install.sh was removed
        assert not (target / "install.sh").exists(), "install.sh not removed from target"


def test_install_script_default_target():
    """install.sh must have sensible default target"""
    content = INSTALL_SCRIPT.read_text()
    assert "~/.pi/agent/extensions/ui-consistency" in content, "Missing default target"


if __name__ == "__main__":
    test_install_script_exists()
    test_install_script_is_executable()
    test_install_script_has_shebang()
    test_install_script_has_set_euo()
    test_install_script_creates_target_dir()
    test_install_script_copies_files()
    test_install_script_self_cleanup()
    test_install_script_runs_successfully()
    test_install_script_default_target()
    print("✅ All install script tests pass")
