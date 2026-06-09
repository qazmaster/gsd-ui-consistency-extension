# Workflow: Generate Design System

<required_reading>
- references/complexity-detection.md
- references/design-system-format.md
</required_reading>

<purpose>
Create STYLE_PICK.md, DESIGN_DNA.md, and COMPONENT_PLAN.md from codebase analysis + user input.
Run this when no design system exists in `.gsd/ui-gates/`.
</purpose>

<process>

## Phase 0: Research

**Goal:** Understand current design patterns in the codebase.

1. **Scan for UI files:**
   ```bash
   find src -name "*.tsx" -o -name "*.jsx" -o -name "*.vue" -o -name "*.svelte" | head -100
   find src -name "*.css" -o -name "*.scss" -o -name "*.module.css" | head -100
   ```

2. **Extract current patterns:**
   - Colors: `grep -roh '#[0-9a-fA-F]\{3,8\}\|rgb(a)\?([^)]*)' src/ --include="*.css" --include="*.tsx" | sort | uniq -c | sort -rn | head -20`
   - Fonts: `grep -roh 'font-family:[^;]*' src/ --include="*.css" | sort | uniq -c | sort -rn | head -10`
   - Spacing: `grep -roh '[0-9]\+px\|[0-9]\+rem' src/ --include="*.css" | sort | uniq -c | sort -rn | head -20`
   - Components: `grep -r 'export.*function\|export.*const.*=.*(' src/ --include="*.tsx" --include="*.jsx" | head -30`

3. **Check for existing design system indicators:**
   - Tailwind config: `ls tailwind.config.* 2>/dev/null`
   - CSS variables: `grep -r 'var(--' src/ --include="*.css" | head -10`
   - Design tokens: `find . -name "tokens*" -o -name "theme*" | head -10`
   - Component library: `grep -r 'from.*@radix\|from.*@headlessui\|from.*@chakra\|from.*@mui' src/ --include="*.tsx" | head -5`

4. **Produce RESEARCH.md** with:
   - Stack detected (React/Vue/Svelte, CSS approach)
   - Current color palette (top 10)
   - Current typography (fonts, sizes)
   - Current spacing patterns
   - Component inventory (count, variants)
   - Existing design system indicators

5. **Ask user 3-5 questions** (use ask_user_questions):
   - Vibe/mood: "What feeling should the UI convey?" (professional, playful, minimal, bold)
   - Audience: "Who are the primary users?" (developers, consumers, enterprise, creative)
   - References: "Any sites/apps whose design you admire?" (2-3 examples)
   - Density: "Preferred information density?" (spacious, balanced, dense)
   - Priority: "What matters most?" (consistency, polish, speed, accessibility)

## Phase 1: Generate

**Goal:** Create design system documents.

1. **Create `.gsd/ui-gates/` directory:**
   ```bash
   mkdir -p .gsd/ui-gates
   ```

2. **Generate STYLE_PICK.md** — visual direction:
   - Color palette (primary, secondary, accent, neutral, semantic)
   - Typography scale (headings, body, caption)
   - Spacing scale (4px base or 8px base)
   - Border radius scale
   - Shadow scale
   - Animation/easing defaults
   - Based on: RESEARCH.md patterns + user answers

3. **Generate DESIGN_DNA.md** — personality:
   - Density preference (spacious/balanced/dense)
   - Trust signals (formal/friendly/playful)
   - Visual rhythm (grid, whitespace patterns)
   - Anti-patterns to avoid
   - Accessibility baseline

4. **Generate COMPONENT_PLAN.md** — component specs:
   - Shell structure for each component type
   - State variants (default, hover, active, disabled, loading, error)
   - Size variants (sm, md, lg)
   - Composition patterns
   - Verification checklist per component

5. **Gate: Present to user for review.**
   - Show generated files
   - Ask: "Adjust anything, or approve to continue?"
   - Wait for approval before proceeding to Phase 2

</process>

<success_criteria>
- `.gsd/ui-gates/STYLE_PICK.md` exists with color/typography/spacing scales
- `.gsd/ui-gates/DESIGN_DNA.md` exists with personality and anti-patterns
- `.gsd/ui-gates/COMPONENT_PLAN.md` exists with component specs
- User has reviewed and approved
- RESEARCH.md saved in `.gsd/workflows/ui-consistency/YYYY-MM-DD/`
</success_criteria>
