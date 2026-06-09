# UI Consistency Extension for GSD

A global GSD extension that provides UI/UX consistency tooling — design system generation, drift detection, and wave-based remediation.

## Features

- **Design System Generation** — Auto-generate `STYLE_PICK.md`, `DESIGN_DNA.md`, and `COMPONENT_PLAN.md` from your codebase
- **Drift Detection** — Scan UI files and classify them as modern, legacy, drift, or unknown
- **Audit** — Check UI files against the design system with severity-ranked findings
- **Fix** — Apply automated fixes (simple/medium modes) or generate audit reports (hard mode)
- **Auto-injection** — Design system context is automatically injected for UI-related tasks

## Prerequisites

- **Node.js** ≥ 20 (required for TypeScript compilation)
- **Python** 3 (required for running tests)
- **GSD CLI** installed globally (`npm install -g @gsd/pi` or equivalent)

## Installation

```bash
# From local path (development)
gsd install ~/.gsd/agent/extensions/ui-consistency

# From git (when published)
gsd install git:github.com/qazmaster/gsd-ui-consistency-extension@v1

# Try without installing
gsd -e ~/.gsd/agent/extensions/ui-consistency
```

## Commands

| Command | Description |
|---------|-------------|
| `/ui-consistency scan [path]` | Scan and classify UI files |
| `/ui-consistency audit [path]` | Audit against design system |
| `/ui-consistency generate` | Generate design system documents |
| `/ui-consistency fix <file>` | Apply fixes to a file |

## Tools (LLM-callable)

| Tool | Purpose |
|------|---------|
| `ui_consistency_scan` | Scan UI files and classify them |
| `ui_consistency_audit` | Audit files against design system |
| `ui_consistency_generate_design_system` | Generate design system from codebase |
| `ui_consistency_fix` | Apply fixes to a specific file |

## Hooks

- **session_start** — Checks for design system and shows status in footer
- **before_agent_start** — Injects design system context for UI-related tasks

## Workflow Template

The extension includes a `ui-consistency` workflow template (markdown-phase, 6 phases):

1. **Research** — Analyze codebase + ask user design questions
2. **Generate** — Create STYLE_PICK.md, DESIGN_DNA.md, COMPONENT_PLAN.md
3. **Scan** — Find all UI files, classify, count metrics
4. **Audit** — Check each file against design system, prioritize findings
5. **Fix** — Apply fixes (complexity-dependent) or generate AUDIT.md
6. **Verify** — Re-scan, browser screenshots, before/after comparison

Usage:
```bash
/gsd start ui-consistency
```

## Complexity Modes

| Mode | File Count | Behavior |
|------|-----------|----------|
| Simple | < 50 | Fix all issues inline |
| Medium | 50–200 | Fix tokens only, rest via refactor |
| Hard | > 200 | Audit only, no code changes |

Override with flags: `--fix`, `--fix-tokens`, `--audit-only`

## Artifacts

Design system artifacts are written to `.gsd/ui-gates/`:
- `STYLE_PICK.md` — Visual direction (colors, typography, spacing)
- `DESIGN_DNA.md` — Design personality (mood, density, anti-patterns)
- `COMPONENT_PLAN.md` — Component specs (states, sizes, verification)

Workflow artifacts go to `.gsd/workflows/ui-consistency/YYYY-MM-DD/`:
- `RESEARCH.md`, `INVENTORY.md`, `AUDIT.md`, `PRIORITY.md`
- `METRICS.json`, `inventory.json`, `UI_VERIFY.json`

## Configuration

No configuration required. The extension auto-detects:
- Framework (React, Vue, Svelte, etc.)
- CSS approach (Tailwind, CSS modules, etc.)
- Complexity by file count

Optional: Set `uiConsistency.designSystem.base` in `~/.gsd/PREFERENCES.md` for token inheritance.

## Development

```bash
# Install dependencies
npm install

# Type-check the extension
npx tsc --noEmit

# Test without installing
gsd -e .

# Or install locally
./install.sh

# Reload extension after changes (inside GSD)
/reload
```

## Tests

The extension includes 14 automated tests covering structure, validation, and consistency:

```bash
cd skills/ui-consistency/tests
python3 run_all_tests.py
```

| Test Suite | Coverage |
|-----------|----------|
| `test_extension_package_structure.py` | Directory structure, required files |
| `test_extension_manifest_valid.py` | extension-manifest.json schema |
| `test_package_json_valid.py` | package.json + pi manifest |
| `test_index_ts_valid.py` | TypeScript entry point registrations |
| `test_workflow_template_valid.py` | Workflow template completeness |
| `test_skill_integrity.py` | SKILL.md, workflows, references |
| `test_install_script.py` | install.sh correctness |
| `test_cross_reference_consistency.py` | Cross-file consistency |
| `test_ui_verify_contract.py` | UI_VERIFY.json schema |
| `test_token_inheritance_path.py` | Token config path |
| `test_no_fake_features.py` | No unimplemented config |
| `test_no_duplicate_flags.py` | Flag uniqueness |
| `test_single_approval_gate.py` | Single gate in workflow |
| `test_unknown_classification.py` | Unknown classification docs |

## Package Structure

```
ui-consistency/
├── package.json                    # pi manifest
├── extension-manifest.json         # Capability declaration
├── index.ts                        # Extension entry point (680 lines)
├── README.md                       # Documentation
├── install.sh                      # One-command installer
├── prompts/
│   └── ui-consistency.md           # Workflow template
└── skills/
    └── ui-consistency/
        ├── SKILL.md                # Skill definition
        ├── workflows/              # 4 workflow files
        ├── references/             # 5 reference docs
        └── tests/                  # 14 test files + runner
```

## License

MIT
