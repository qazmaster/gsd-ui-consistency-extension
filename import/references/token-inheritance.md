# Token-Level Inheritance

## Overview

Multi-project design system via token-level inheritance. Base = optional company brandbook.
Project = source of truth for everything except tokens.

## Architecture

```
~/.gsd/shared-design/tokens/        ← Base (optional, user creates manually)
  colors.json
  typography.json
  spacing.json

project/.gsd/ui-gates/tokens/       ← Merged result (workflow creates)
  colors.json                       ← base + project overrides
  typography.json
  spacing.json

project/.gsd/ui-gates/
  STYLE_PICK.md                     ← Project-only (references merged tokens)
  DESIGN_DNA.md                     ← Project-only
  COMPONENT_PLAN.md                 ← Project-only
```

## Who Creates What

| Artifact | Creator | Location |
|----------|---------|----------|
| Base tokens | User (manual) | `~/.gsd/shared-design/tokens/` |
| Project design system | Workflow | `project/.gsd/ui-gates/` |
| Merged tokens | Workflow | `project/.gsd/ui-gates/tokens/` |

## Config

```yaml
# project/.gsd/PREFERENCES.md
uiConsistency:
  designSystem:
    path: .gsd/ui-gates/
    autoGenerate: true
    base: ~/.gsd/shared-design/tokens/  # Optional: path to shared tokens
```

The workflow reads `uiConsistency.designSystem.base` from `.gsd/PREFERENCES.md`.

## Merge Logic

During Phase 2 (Generate):

1. Check if `designSystem.base` is set and directory exists
2. If yes: load base tokens (colors, typography, spacing)
3. Merge: project values override base values
4. Save merged result to `.gsd/ui-gates/tokens/`
5. Generate STYLE_PICK.md referencing merged tokens

### Merge Rules

- **Colors:** project overrides base per key (primary, secondary, etc.)
- **Typography:** project overrides font-family, scale; base provides fallbacks
- **Spacing:** project overrides base unit and scale
- **New keys:** project-only keys are preserved as-is

### Example

Base (`~/.gsd/shared-design/tokens/colors.json`):
```json
{
  "primary": "#0066CC",
  "neutral": "#333333",
  "company-accent": "#FF6600"
}
```

Project (from RESEARCH.md):
```json
{
  "primary": "#4F8AFF",
  "success": "#2ECA7F"
}
```

Merged (`.gsd/ui-gates/tokens/colors.json`):
```json
{
  "primary": "#4F8AFF",
  "neutral": "#333333",
  "company-accent": "#FF6600",
  "success": "#2ECA7F"
}
```

## When to Read Base

| Actor | Reads Base? | Reads Merged? |
|-------|-------------|---------------|
| Workflow (generate phase) | Yes, via `uiConsistency.designSystem.base` | No (creates it) |
| GSD auto-mode | No | Yes |
| LLM (via skill) | No | Yes |

## Base Token File Format

Base tokens directory structure:
```
~/.gsd/shared-design/tokens/
├── colors.json         # { "primary": "#...", "secondary": "#..." }
├── typography.json     # { "fontFamily": "...", "scale": { "h1": "32px" } }
└── spacing.json        # { "baseUnit": "4px", "scale": { "xs": "4px" } }
```

All files optional. Missing files are skipped during merge.

## Documentation

This feature must be documented in:
1. SKILL.md (reference_index)
2. workflow template (Phase 2 step 2)
3. PREFERENCES.md (designSystem.base field)
