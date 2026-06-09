# Complexity Detection

## Heuristics

Run these commands to assess project complexity:

```bash
# Count UI component files
find src -name "*.tsx" -o -name "*.jsx" -o -name "*.vue" -o -name "*.svelte" | wc -l

# Count CSS/style files
find src -name "*.css" -o -name "*.scss" -o -name "*.module.css" | wc -l

# Check for Tailwind
ls tailwind.config.* 2>/dev/null && echo "tailwind: yes" || echo "tailwind: no"

# Check for CSS variables usage
grep -r "var(--" src/ --include="*.css" --include="*.scss" | wc -l

# Check CSS-in-JS approaches
ls src/ | grep -E "styled|emotion|css-modules" | head -5

# Count component variants (exported components)
grep -r "export.*function\|export.*const.*=.*(" src/ --include="*.tsx" --include="*.jsx" | wc -l

# Check for design system imports
grep -r "from.*design-system\|from.*@theme\|from.*tokens" src/ --include="*.tsx" | wc -l
```

## Levels

| Level | Component Files | CSS Approach | Variants | Est. Time |
|-------|----------------|--------------|----------|-----------|
| **Simple** | <50 | Tailwind (single config) or CSS vars | <3 per component | 1-2 days |
| **Medium** | 50-200 | Mixed or no unified system | 3-5 per component | 1-2 weeks |
| **Hard** | >200 | Monorepo, multiple apps, mixed approaches | >5 per component | 1-2 months |

## Mode Selection

```
if component_files < 50:
    mode = "simple"     # audit + fix all
elif component_files < 200:
    mode = "medium"     # audit + fix tokens, rest via refactor
else:
    mode = "hard"       # audit only, no code changes
```

## Override Flags

User can override auto-detection:
- `--audit-only` → hard mode regardless of count
- `--fix` → simple mode regardless of count
- `--fix-tokens` → medium mode regardless of count

## Wave Size by Complexity

| Complexity | Files per Wave | Waves |
|------------|---------------|-------|
| Simple | 10-15 | 3-5 |
| Medium | 5-10 | 5-10 |
| Hard | 3-5 (audit only) | N/A |
