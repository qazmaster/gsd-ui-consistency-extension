# UI Consistency Import Package

## Purpose

This package contains the unified UI consistency skill and workflow that can be safely imported into any GSD project **on top of** existing stock GSD files.

## Import Strategy: Append, Don't Overwrite

The import uses **append-only** strategy to avoid conflicts with stock GSD:

1. **SKILL.md** → Append new sections to existing skill file
2. **Workflows** → Add new workflow files (don't touch stock)
3. **PREFERENCES.md** → Append new config blocks
4. **References** → Add new reference docs

## Files

```
import/
├── README.md                    # This file
├── SKILL.md.patch               # Sections to append to skill
├── workflows/                   # New workflow files
│   └── full-pipeline.md
├── references/                  # New reference docs
│   ├── complexity-detection.md
│   ├── design-system-format.md
│   ├── legacy-classification.md
│   ├── token-inheritance.md
│   └── wave-planning.md
└── config/
    └── PREFERENCES.md.patch     # Config blocks to append
```

## Quick Import

```bash
# 1. Copy workflows
cp import/workflows/*.md ~/.gsd/agent/skills/ui-consistency/workflows/

# 2. Copy references
cp import/references/*.md ~/.gsd/agent/skills/ui-consistency/references/

# 3. Append SKILL.md sections
cat import/SKILL.md.patch >> ~/.gsd/agent/skills/ui-consistency/SKILL.md

# 4. Append PREFERENCES.md config
cat import/config/PREFERENCES.md.patch >> ~/.gsd/PREFERENCES.md
```

## Safety Checks

Before import, verify:
- [ ] Stock GSD files exist (don't create from scratch)
- [ ] No duplicate sections (check if already imported)
- [ ] Backup created: `cp -r ~/.gsd/agent/skills/ui-consistency ~/.gsd/agent/skills/ui-consistency.bak`

## Post-Import Verification

```bash
# Run tests
python3 ~/.agents/skills/ui-consistency/tests/run_all_tests.py

# Check skill routing
skill_routing_health
```
