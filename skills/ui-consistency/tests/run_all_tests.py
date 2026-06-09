#!/usr/bin/env python3
"""Run all UI consistency tests — bug-fix + extension package"""

import subprocess
import sys
from pathlib import Path

TESTS = [
    # Original bug-fix tests
    "test_ui_verify_contract.py",
    "test_token_inheritance_path.py",
    "test_no_fake_features.py",
    "test_no_duplicate_flags.py",
    "test_single_approval_gate.py",
    "test_unknown_classification.py",
    # Extension package tests
    "test_extension_package_structure.py",
    "test_extension_manifest_valid.py",
    "test_package_json_valid.py",
    "test_index_ts_valid.py",
    "test_workflow_template_valid.py",
    "test_skill_integrity.py",
    "test_install_script.py",
    "test_cross_reference_consistency.py",
]


def main():
    test_dir = Path(__file__).parent
    passed = 0
    failed = 0
    skipped = 0

    for test in TESTS:
        test_path = test_dir / test
        if not test_path.exists():
            print(f"\n⚠️  SKIP: {test} (not found)")
            skipped += 1
            continue

        print(f"\n{'='*60}")
        print(f"Running: {test}")
        print("=" * 60)

        result = subprocess.run(
            [sys.executable, str(test_path)],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            print(f"✅ PASS: {test}")
            if result.stdout.strip():
                print(f"   {result.stdout.strip()}")
            passed += 1
        else:
            print(f"❌ FAIL: {test}")
            if result.stdout.strip():
                print(result.stdout)
            if result.stderr.strip():
                print(result.stderr)
            failed += 1

    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed, {skipped} skipped")
    print("=" * 60)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
