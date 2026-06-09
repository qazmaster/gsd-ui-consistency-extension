# Design System Format

## File Locations

```
.gsd/ui-gates/
├── STYLE_PICK.md       # Visual direction
├── DESIGN_DNA.md       # Personality, density, trust
├── COMPONENT_PLAN.md   # Component specs
└── UI_VERIFY.json      # Verification evidence
```

## STYLE_PICK.md Structure

```markdown
# Style Pick

## Color Palette
- Primary: {hex} — main brand color
- Secondary: {hex} — supporting color
- Accent: {hex} — call-to-action, highlights
- Neutral: {hex} — text, borders, backgrounds
- Semantic: success={hex}, warning={hex}, error={hex}, info={hex}

## Typography
- Font family: {family} (headings), {family} (body)
- Scale: h1={size}, h2={size}, h3={size}, body={size}, caption={size}
- Line height: {value}
- Font weights: regular={weight}, medium={weight}, bold={weight}

## Spacing
- Base unit: {4px|8px}
- Scale: xs={n}, sm={n}, md={n}, lg={n}, xl={n}, 2xl={n}

## Border Radius
- Scale: sm={n}px, md={n}px, lg={n}px, full=9999px

## Shadows
- Scale: sm={value}, md={value}, lg={value}

## Animation
- Duration: fast=150ms, normal=300ms, slow=500ms
- Easing: default={value}, enter={value}, exit={value}
```

## DESIGN_DNA.md Structure

```markdown
# Design DNA

## Personality
- Mood: {professional|playful|minimal|bold}
- Trust signals: {formal|friendly|playful}

## Density
- Preference: {spacious|balanced|dense}
- Whitespace: {generous|moderate|tight}

## Visual Rhythm
- Grid: {8px|4px} base
- Content width: {max-width}
- Section spacing: {value}

## Anti-Patterns
- Avoid: {list of things to never do}
- Prefer: {list of things to always do}

## Accessibility
- Contrast ratio: {4.5:1 minimum}
- Focus indicators: {visible|subtle}
- Touch targets: {44px minimum}
```

## COMPONENT_PLAN.md Structure

```markdown
# Component Plan

## Button
### Shell
- Container → Label → Icon (optional)
### States
- default, hover, active, disabled, loading
### Sizes
- sm (height: 32px), md (height: 40px), lg (height: 48px)
### Variants
- primary, secondary, ghost, danger
### Verification
- [ ] Uses design tokens for colors
- [ ] Follows spacing scale
- [ ] Has ARIA labels
- [ ] Keyboard accessible

## Input
### Shell
- Container → Label → Field → Helper text (optional)
### States
- default, focus, error, disabled
...
```

## UI_VERIFY.json Structure

Must use `schemaVersion: "ui-verify.fixture.v1"` for compatibility with `ui_ux_validate_gate_pack`.

```json
{
  "schemaVersion": "ui-verify.fixture.v1",
  "evidenceFresh": true,
  "metadata": {
    "notApplicableArtifacts": ["PRIME_DIRECTION.json", "STRUCTURAL_REVIEW.json", "OPTICAL_REVIEW.json", "PROVENANCE_TRACKING.json"],
    "workflow": "ui-consistency",
    "workflowVersion": "YYYY-MM-DD"
  },
  "routes": [
    { "path": "/", "status": "pass" },
    { "path": "/sites", "status": "pass" }
  ],
  "viewports": {
    "desktop": { "status": "pass" },
    "tablet": { "status": "pass" },
    "mobile": { "status": "pass" }
  },
  "console": { "status": "pass" },
  "network": { "status": "pass" },
  "horizontalOverflow": { "status": "pass" },
  "focusVisibility": { "status": "pass" },
  "uiVerdict": "PASS",
  "verdictRationale": "One sentence explaining the verdict.",
  "checks": {
    "colorConsistency": { "status": "pass", "evidence": "Description" },
    "spacingScale": { "status": "warning", "evidence": "Description" }
  },
  "nextSteps": ["Step 1", "Step 2"]
}
```

### Required Fields

| Field | Type | Values | Notes |
|-------|------|--------|-------|
| `schemaVersion` | string | `"ui-verify.fixture.v1"` | Must match exactly |
| `evidenceFresh` | boolean | `true` | Must be `true` for valid evidence |
| `routes` | array | `[{path, status}]` | At least one route required |
| `viewports` | object | `{desktop, tablet, mobile}` | All three required |
| `console` | object | `{status}` | Required |
| `network` | object | `{status}` | Required |
| `horizontalOverflow` | object | `{status}` | Required |
| `focusVisibility` | object | `{status}` | Required |
| `uiVerdict` | string | `PASS`, `FAIL`, `NEEDS_ATTENTION` | Overall verdict |

### Status Values

Each check status can be:
- `"pass"` — check passed
- `"fail"` or `"blocked"` — check failed
- `"warning"` or `"needs-attention"` — needs attention
- `{ "status": "skipped", "reason": "..." }` — skipped with reason

### Not-Applicable Artifacts

For ui-consistency workflow, these are not applicable:
- `PRIME_DIRECTION.json` — creative mode only
- `STRUCTURAL_REVIEW.json` — creative mode only
- `OPTICAL_REVIEW.json` — creative mode only
- `PROVENANCE_TRACKING.json` — public-facing only

List them in `metadata.notApplicableArtifacts`.

## Compatibility with ui-gates Tools

These files are read by:
- `ui_ux_validate_gate_pack` — validates UI_VERIFY.json schema + required fields
- `ui_ux_source_scan` — cross-references code against STYLE_PICK
- `ui_ux_browser_plan` — generates verification routes
- `ui_ux_optical_review` — checks visual consistency

Always generate files in this format for tool compatibility.
