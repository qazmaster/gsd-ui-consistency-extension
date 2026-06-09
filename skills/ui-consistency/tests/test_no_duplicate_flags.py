#!/usr/bin/env python3
"""Test: No duplicate flags in workflow template"""

import re
from pathlib import Path

WORKFLOW = Path("~/.gsd/agent/extensions/gsd/workflow-templates/ui-consistency.md").expanduser()


def test_no_duplicate_classify_flag():
    """--classify flag must appear only once in <flags> section"""
    content = WORKFLOW.read_text()

    flags_section = re.search(r'<flags>(.*?)</flags>', content, re.DOTALL)
    assert flags_section, "Flags section not found"

    flags = flags_section.group(1)
    classify_count = len(re.findall(r'--classify', flags))

    assert classify_count == 1, \
        f"--classify flag appears {classify_count} times, expected 1"


if __name__ == "__main__":
    test_no_duplicate_classify_flag()
    print("✅ No duplicate flags test passes")
