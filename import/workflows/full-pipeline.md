# Workflow: Full UI Consistency Pipeline

<required_reading>
- references/complexity-detection.md
- references/design-system-format.md
- references/wave-planning.md
</required_reading>

<purpose>
Complete end-to-end UI consistency workflow: research → generate → scan → audit → fix → verify.
Use this for comprehensive UI audits when starting from scratch or doing a full redesign.
</purpose>

<process>

## Phase 0: Research

**Goal:** Understand current design patterns and user intent.

1. **Detect stack:**
   ```bash
   # Framework
   ls package.json && cat package.json | grep -E "react|vue|svelte|angular|next|nuxt"

   # CSS approach
   ls tailwind.config.* 2>/dev/null
   ls postcss.config.* 2>/dev/null

   # Component files
   find src -name "*.tsx" -o -name "*.jsx" -o -name "*.vue" -o -name "*.svelte" 2>/dev/null | wc -l

   # Style files
   find src -name "*.css" -o -name "*.scss" -o -name "*.module.css" 2>/dev/null | wc -l
   ```

2. **Extract current patterns:**
   ```bash
   # Colors (top 10)
   grep -roh '#[0-9a-fA-F]\{3,8\}' src/ --include="*.css" --include="*.tsx" 2>/dev/null | sort | uniq -c | sort -rn | head -10

   # Fonts
   grep -roh 'font-family:[^;]*' src/ --include="*.css" 2>/dev/null | sort | uniq -c | sort -rn | head -5

   # Spacing (top 10 px values)
   grep -roh '[0-9]\+px' src/ --include="*.css" 2>/dev/null | sort | uniq -c | sort -rn | head -10

   # CSS variables
   grep -r 'var(--' src/ --include="*.css" --include="*.tsx" 2>/dev/null | wc -l

   # Inline styles
   grep -r 'style={{' src/ --include="*.tsx" 2>/dev/null | wc -l
   ```

3. **Check existing design system:**
   ```bash
   ls .gsd/ui-gates/STYLE_PICK.md 2>/dev/null
   ls .gsd/ui-gates/DESIGN_DNA.md 2>/dev/null
   ls .gsd/ui-gates/COMPONENT_PLAN.md 2>/dev/null
   ```

4. **Write `RESEARCH.md`** with:
   - Stack detected (framework, CSS approach)
   - Current color palette (top 10)
   - Current typography (fonts)
   - Current spacing patterns
   - CSS variable usage count
   - Inline style count
   - Existing design system: yes/no

5. **Ask user 3-5 questions** (use ask_user_questions):
   - Vibe/mood: "What feeling should the UI convey?" (professional, playful, minimal, bold)
   - Audience: "Who are the primary users?" (developers, consumers, enterprise, creative)
   - References: "Any sites/apps whose design you admire?" (2-3 examples)
   - Density: "Preferred information density?" (spacious, balanced, dense)
   - Priority: "What matters most?" (consistency, polish, speed, accessibility)

6. **Assess complexity** (auto-detection):
   ```
   if component_files < 50:
       complexity = "simple"     # audit + fix all
   elif component_files < 200:
       complexity = "medium"     # audit + fix tokens, rest via refactor
   else:
       complexity = "hard"       # audit only, no code changes
   ```
   Override with `--audit-only`, `--fix`, `--fix-tokens` flags.

7. **Recommendation:** Present findings and complexity to user. Confirm to proceed before moving to Phase 1.

## Phase 1: Generate

**Goal:** Create design system documents from research + user input.

1. **Create directory:**
   ```bash
   mkdir -p .gsd/ui-gates
   ```

2. **Check for base design tokens** (token-level inheritance):
   - Read `uiConsistency.designSystem.base` from `.gsd/PREFERENCES.md`
   - If set (e.g. `~/.gsd/shared-design/tokens/`) and directory exists:
     - Load base tokens (colors, typography, spacing)
     - Merge with project-specific values (project overrides base)
     - Save merged result to `.gsd/ui-gates/tokens/`
   - If empty, missing, or directory doesn't exist:
     - Generate project-only tokens
     - Save to `.gsd/ui-gates/tokens/`

3. **Generate `STYLE_PICK.md`** — visual direction:
   - Color palette: primary, secondary, accent, neutral, semantic
   - Typography: font family, scale, line height, weights
   - Spacing: base unit (4px or 8px), scale
   - Border radius: scale
   - Shadows: scale
   - Animation: duration, easing defaults
   - Based on: RESEARCH.md patterns + user answers

4. **Generate `DESIGN_DNA.md`** — personality:
   - Mood, trust signals, density
   - Visual rhythm, anti-patterns
   - Accessibility baseline

5. **Generate `COMPONENT_PLAN.md`** — component specs:
   - Shell structure, state variants, size variants
   - Verification checklist per component

6. **Write files** to `.gsd/ui-gates/`

7. **Gate:** Present to user. Ask: "Adjust anything, or approve to continue?"

## Phase 2: Scan

**Goal:** Find all UI files and classify them.

1. **Verify design system exists:**
   ```bash
   ls .gsd/ui-gates/STYLE_PICK.md .gsd/ui-gates/DESIGN_DNA.md .gsd/ui-gates/COMPONENT_PLAN.md
   ```

2. **Find all UI files:**
   ```bash
   find src -name "*.tsx" -o -name "*.jsx" -o -name "*.vue" -o -name "*.svelte" \
     -o -name "*.css" -o -name "*.scss" -o -name "*.module.css" -o -name "*.html" \
     | sort > /tmp/ui-files.txt
   ```

3. **Classify each file:**
   - **modern:** uses CSS variables/tokens, imports from design system
   - **legacy:** hardcoded colors, inline styles
   - **drift:** mixed patterns
   - **unknown:** no UI indicators

4. **Write `INVENTORY.md`** and **`inventory.json`**

5. **Write `METRICS.json`**

## Phase 3: Audit

**Goal:** Check each file against design system, find anti-patterns, prioritize.

1. **For each file, check:**
   - Color usage: hardcoded vs tokens
   - Typography: vs design system
   - Spacing: px values vs scale
   - Component patterns: follows COMPONENT_PLAN?
   - Accessibility: ARIA, keyboard nav, contrast

2. **Use tools if available:**
   - `ui_ux_source_scan` for automated findings
   - `ui_ux_structural_review` for layout
   - `ui_ux_optical_review` for visual polish

3. **Write `AUDIT.md`** with findings

4. **Write `PRIORITY.md`** with ranked fix list

## Phase 4: Fix

**Complexity-dependent:**

**Simple mode (< 50 files):**
- Fix all waves
- Replace hardcoded colors with tokens
- Replace inline styles with classes
- Add missing ARIA labels
- Record in `PROGRESS.md`

**Medium mode (50-200 files):**
- Fix Wave 1 (tokens) only
- Write `PROGRESS.md`
- Recommend refactor for rest

**Hard mode (> 200 files):**
- STRICTLY NO FILE MODIFICATIONS
- Generate detailed AUDIT.md + PRIORITY.md
- Recommend refactor workflow

## Phase 5: Verify

**Goal:** Confirm fixes work, no new drift.

1. **Re-scan modified files**
2. **Update `inventory.json`**
3. **Write `UI_VERIFY.json`**
4. **Browser verification** (if app running)
5. **Write `BEFORE_AFTER.md`**
6. **Update `METRICS.json`**

</process>

<success_criteria>
- `.gsd/ui-gates/STYLE_PICK.md` exists with color/typography/spacing scales
- `.gsd/ui-gates/DESIGN_DNA.md` exists with personality
- `.gsd/ui-gates/COMPONENT_PLAN.md` exists with component specs
- `.gsd/ui-gates/RESEARCH.md` exists with codebase analysis
- `.gsd/ui-gates/INVENTORY.md` exists with file classification
- `.gsd/ui-gates/AUDIT.md` exists with findings
- `.gsd/ui-gates/PRIORITY.md` exists with ranked fix list
- `.gsd/ui-gates/UI_VERIFY.json` exists with verification evidence
- User has reviewed and approved design system
- Build passes after fixes (if any applied)
</success_criteria>

<outputs>
Artifacts in `.gsd/ui-gates/`:

| Phase | Artifact | Description |
|-------|----------|-------------|
| 0 | RESEARCH.md | Codebase analysis + user input |
| 1 | STYLE_PICK.md | Visual direction |
| 1 | DESIGN_DNA.md | Design personality |
| 1 | COMPONENT_PLAN.md | Component specs |
| 1 | tokens/ | Design tokens (if base inheritance used) |
| 2 | INVENTORY.md | All UI files with classification |
| 2 | METRICS.json | Quantitative metrics |
| 2 | inventory.json | Classification registry |
| 3 | AUDIT.md | Detailed audit findings |
| 3 | PRIORITY.md | Ranked fix list |
| 4 | PROGRESS.md | Progress per wave (if fixes applied) |
| 5 | BEFORE_AFTER.md | Comparison report |
| 5 | UI_VERIFY.json | Verification evidence |
| 5 | METRICS.json | Updated metrics (post-fix) |
</outputs>
