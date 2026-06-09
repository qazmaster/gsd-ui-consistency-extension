# Wave Planning

## Principles

1. **Each wave leaves codebase working** — never break the build between waves
2. **Dependencies first** — change definitions before consumers
3. **Verify between waves** — build + test after each wave
4. **Atomic commits** — each wave = one commit (with --create-branch)

## Standard Wave Order

```
Wave 1: Tokens (colors, fonts, spacing)
  → CSS variables, Tailwind config, theme files
  → Easy, high impact, low risk

Wave 2: Core Components (Button, Input, Card)
  → Replace hardcoded values with tokens
  → Medium effort, high visibility

Wave 3: Layout (Grid, Container, breakpoints)
  → Spacing alignment, responsive patterns
  → Medium effort

Wave 4: Page-level Components
  → Full alignment of page compositions
  → Hard effort, high risk
```

## Wave Size by Complexity

| Complexity | Files per Wave | Rationale |
|------------|---------------|-----------|
| Simple | 10-15 | Can verify all at once |
| Medium | 5-10 | Incremental verification |
| Hard | 3-5 | Minimize blast radius |

## Dependency Analysis

Before planning waves, check:
1. **Import graph:** Which files import from which?
2. **Token dependencies:** Which files define tokens vs consume them?
3. **Component hierarchy:** Parent components before children?

```bash
# Find token definitions
grep -rn 'export.*const.*tokens\|export.*theme\|--color-' src/ --include="*.ts" --include="*.css" | head -10

# Find token consumers
grep -rn 'import.*tokens\|import.*theme\|var(--' src/ --include="*.tsx" --include="*.css" | wc -l
```

## Parallel Waves

If directories are independent, waves can run in parallel:
```
Wave 1a: src/components/ tokens (independent)
Wave 1b: src/pages/ tokens (independent)
→ Can run simultaneously

Wave 2: src/components/ core (depends on Wave 1a)
→ Must wait for Wave 1a
```

## Wave Commit Messages

With `--create-branch`:
```
ui(tokens): wave 1 — replace hardcoded colors with design tokens
ui(components): wave 2 — align Button/Input with STYLE_PICK
ui(layout): wave 3 — spacing grid alignment
ui(pages): wave 4 — page-level consistency fixes
```

## Rollback

- **Without --create-branch:** `git checkout .` or `git stash`
- **With --create-branch:** `git checkout main` (abandon branch)
- **After commit:** `git revert <commit-hash>`
