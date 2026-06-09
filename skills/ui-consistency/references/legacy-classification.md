# Legacy Classification

## Indicators

### Modern Indicators
- Uses CSS variables/tokens (`var(--color-primary)`)
- Imports from design system (`import { Button } from '@/design-system'`)
- Follows STYLE_PICK spacing/typography scales
- Uses component library (Radix, Headless UI, etc.)
- Consistent naming conventions

### Legacy Indicators
- Hardcoded colors (`#fff`, `rgb(255,0,0)`, `color: red`)
- Inline styles (`style={{ padding: '10px' }}`)
- Absolute px values (`width: 150px`) instead of rem/em
- Old React patterns (class components, HOC)
- No imports from design system
- Duplicate component definitions

### Drift Indicators
- Mixed patterns (partial tokens + partial hardcoded)
- Some components modern, same file has legacy
- Inconsistent spacing (mix of 8px grid + random values)
- Typography doesn't match scale

## Detection Commands

```bash
# Hardcoded colors
grep -rn '#[0-9a-fA-F]\{3,8\}\|rgb(a)\?([^)]*)\|color:.*red\|color:.*blue' src/ \
  --include="*.tsx" --include="*.jsx" --include="*.css" | wc -l

# Inline styles (React)
grep -rn 'style={{' src/ --include="*.tsx" --include="*.jsx" | wc -l

# Hardcoded px (not in Tailwind)
grep -rn '[0-9]\+px' src/ --include="*.css" --include="*.scss" | wc -l

# Class components
grep -rn 'extends React.Component\|extends Component' src/ --include="*.tsx" --include="*.jsx" | wc -l

# Design system imports
grep -rL 'from.*design-system\|from.*@theme\|from.*tokens' src/ --include="*.tsx" | wc -l
```

## Classification Logic

```
For each file:
    if has_modern_indicators AND NOT has_legacy_indicators:
        classification = "modern"
    elif has_legacy_indicators AND NOT has_modern_indicators:
        classification = "legacy"
    elif has_modern_indicators AND has_legacy_indicators:
        classification = "drift"
    else:
        classification = "unknown"  # needs manual review
```

## Enforcement by Classification

| Classification | Enforcement | Action |
|---------------|-------------|--------|
| Modern | Strict | Must follow STYLE_PICK |
| Legacy | Advisory | Track in inventory, migrate on touch |
| Drift | Warn | Warn if modified but not migrated |
| Unknown | None | No UI indicators; skip enforcement |

## Inventory.json Format

Stored in `.gsd/ui-gates/inventory.json`. Updated after each scan.

```json
{
  "src/components/Button.tsx": {
    "classification": "modern",
    "lastScan": "2026-06-09",
    "stylePickVersion": "v1",
    "reason": "uses design system patterns"
  },
  "src/components/OldModal.tsx": {
    "classification": "legacy",
    "lastScan": "2026-06-09",
    "stylePickVersion": "v1",
    "reason": "12 hardcoded colors, 8 inline styles"
  },
  "src/components/Dashboard/Card.tsx": {
    "classification": "drift",
    "lastScan": "2026-06-09",
    "stylePickVersion": "v1",
    "reason": "4 hardcoded colors"
  },
  "src/utils/helpers.ts": {
    "classification": "unknown",
    "lastScan": "2026-06-09",
    "stylePickVersion": "v1",
    "reason": "no UI indicators"
  }
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `classification` | string | `modern`, `legacy`, `drift`, or `unknown` |
| `lastScan` | string | ISO date of last scan |
| `stylePickVersion` | string | STYLE_PICK version used for classification |
| `reason` | string | Why this classification was assigned |

### Update Rules

- After scan (Phase 3): full regeneration from scratch
- After fix (Phase 4): re-classify fixed files (legacy → modern)
- After STYLE_PICK version change: full rescan all files
- Lazy update after refactor: inventory updates at next scan
