# UI/UX Consistency Workflow (DEPRECATED)

> **DEPRECATED:** This workflow template is deprecated. Use the `ui-consistency` skill instead.
> The skill provides better integration with GSD auto-mode, unified artifact directory (`.gsd/ui-gates/`),
> and proper guard layer via `ui-ux-uat-gates`.
>
> To use: simply mention "check UI consistency" or "audit design system" and the skill will route automatically.

<template_meta>
name: ui-consistency
version: 1
mode: markdown-phase
requires_project: false
artifact_dir: .gsd/ui-gates/
deprecated: true
replacement: ui-consistency skill
</template_meta>

<purpose>
DEPRECATED: Use ui-consistency skill instead. This template is kept for backward compatibility.
Original purpose: Ensure visual and behavioral consistency across all UI components.
</purpose>

<phases>
0. research  — Analyze codebase + ask user design questions
1. generate  — Create STYLE_PICK.md, DESIGN_DNA.md, COMPONENT_PLAN.md
2. scan      — Find all UI files, classify, count metrics
3. audit     — Check each file against design system, prioritize findings
4. fix       — Apply fixes (complexity-dependent) or generate AUDIT.md
5. verify    — Re-scan, browser screenshots, before/after comparison
</phases>

<flags>
--audit-only     Force hard mode (audit only, no code changes)
--fix            Force simple mode (fix all, ignore complexity)
--fix-tokens     Force medium mode (fix tokens only)
--classify=path=class  Manual override: modern|legacy|drift|unknown
--scope=<path>   Restrict to specific files/directory
--from-wave=<N>  Start fix from wave N (skip earlier waves)
--create-branch  Create ui-consistency/YYYY-MM-DD branch for fixes
</flags>

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
   ```bash
   # Read uiConsistency.designSystem.base from PREFERENCES.md
   # If set and directory exists, load base tokens
   # Merge: project tokens override base tokens
   # Save merged tokens to .gsd/ui-gates/tokens/
   ```
   - Read `uiConsistency.designSystem.base` from `.gsd/PREFERENCES.md`
   - If set (e.g. `~/.gsd/shared-design/tokens/`) and directory exists:
     - Load base tokens (colors, typography, spacing)
     - Merge with project-specific values (project overrides base)
     - Save merged result to `.gsd/ui-gates/tokens/`
   - If empty, missing, or directory doesn't exist:
     - Generate project-only tokens
     - Save to `.gsd/ui-gates/tokens/`

3. **Generate `STYLE_PICK.md`** — visual direction:
   - Color palette: primary, secondary, accent, neutral, semantic (success/warning/error/info)
   - Typography: font family, scale (h1-h6, body, caption), line height, weights
   - Spacing: base unit (4px or 8px), scale (xs/sm/md/lg/xl/2xl)
   - Border radius: scale (sm/md/lg/full)
   - Shadows: scale (sm/md/lg)
   - Animation: duration (fast/normal/slow), easing defaults
   - Based on: RESEARCH.md patterns + user answers

4. **Generate `DESIGN_DNA.md`** — personality:
   - Mood: professional/playful/minimal/bold
   - Trust signals: formal/friendly/playful
   - Density: spacious/balanced/dense
   - Visual rhythm: grid base, content width, section spacing
   - Anti-patterns to avoid
   - Accessibility baseline: contrast ratio, focus indicators, touch targets

5. **Generate `COMPONENT_PLAN.md`** — component specs:
   - For each component type: shell structure, state variants, size variants
   - States: default, hover, active, focus, disabled, loading, error
   - Sizes: sm, md, lg
   - Verification checklist per component

6. **Write `STYLE_PICK.md`, `DESIGN_DNA.md`, `COMPONENT_PLAN.md`** to `.gsd/ui-gates/`

7. **Gate:** Present generated files to user. Ask: "Adjust anything, or approve to continue?"
   - Wait for approval before proceeding to Phase 2.
   - User can request changes to color palette, typography, spacing, etc.

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
   wc -l /tmp/ui-files.txt
   ```

3. **Classify each file:**
   - **modern:** uses CSS variables/tokens, imports from design system, follows STYLE_PICK
   - **legacy:** hardcoded colors (#fff, rgb()), inline styles, no design system imports
   - **drift:** mixed patterns (partial tokens + partial hardcoded)
   - **unknown:** no UI indicators (empty file, config file, non-UI utility)

   Classification heuristics:
   ```bash
   # Hardcoded colors
   grep -c '#[0-9a-fA-F]\{3,8\}\|rgb(a)\?([^)]*)' <file>

   # Inline styles
   grep -c 'style={{' <file>

   # CSS variables
   grep -c 'var(--' <file>

   # Design system imports
   grep -c 'from.*design-system\|from.*@theme\|from.*tokens' <file>

   # If none of the above match: classify as "unknown"
   ```

4. **Write `INVENTORY.md`:**
   ```
   # UI File Inventory

   Generated: YYYY-MM-DD
   Total files: N
   Complexity: simple|medium|hard

   ## Classification Summary
   - Modern: N files (X%)
   - Legacy: N files (X%)
   - Drift: N files (X%)
   - Unknown: N files (X%)

   ## File List
   | File | Classification | Reason |
   |------|---------------|--------|
   | src/components/Button.tsx | modern | uses tokens, follows STYLE_PICK |
   | src/components/OldModal.tsx | legacy | inline styles, hardcoded colors |
   | src/utils/helpers.ts | unknown | no UI indicators |
   ```

5. **Write `METRICS.json`:**
   ```json
   {
     "totalFiles": 45,
     "modern": 30,
     "legacy": 10,
     "drift": 4,
     "unknown": 1,
     "complexity": "simple",
     "cssApproach": "tailwind",
     "componentCount": 25,
     "variantCount": 3.2,
     "hardcodedColors": 23,
     "inlineStyles": 12,
     "cssVariables": 385
   }
   ```

6. **Write `inventory.json`** (classification registry):
   ```json
   {
     "src/components/Button.tsx": {
       "classification": "modern",
       "lastScan": "2026-06-09",
       "stylePickVersion": "v1"
     },
     "src/components/OldModal.tsx": {
       "classification": "legacy",
       "lastScan": "2026-06-09",
       "stylePickVersion": "v1",
       "reason": "inline styles, hardcoded colors"
     },
     "src/utils/helpers.ts": {
       "classification": "unknown",
       "lastScan": "2026-06-09",
       "stylePickVersion": "v1",
       "reason": "no UI indicators"
     }
   }
   ```
   Save to `.gsd/ui-gates/inventory.json`

7. **Apply manual overrides** (if `--classify` flag provided):
   ```bash
   # Parse --classify=path=class flag
   # Update inventory.json entry for that path
   # Recalculate INVENTORY.md summary
   ```

8. **Recommendation:** Review INVENTORY.md. Check classification accuracy. Override via `--classify` if needed, then proceed.

## Phase 3: Audit

**Goal:** Check each file against design system, find anti-patterns, prioritize.

1. **For each file, check:**
   - Color usage: hardcoded vs tokens
   - Typography: font-family/font-size vs design system
   - Spacing: px values vs spacing scale
   - Component patterns: follows COMPONENT_PLAN?
   - Accessibility: ARIA labels, keyboard nav, contrast

2. **Use ui-gates tools if available:**
   - `ui_ux_source_scan` for automated findings
   - `ui_ux_structural_review` for layout variety
   - `ui_ux_optical_review` for visual polish

3. **Write `AUDIT.md`:**
   ```
   # UI Consistency Audit

   Date: YYYY-MM-DD
   Mode: simple|medium|hard

   ## Critical Findings
   ### [CRITICAL] src/components/OldModal.tsx
   - Hardcoded colors: #fff, #000, rgb(255,0,0)
   - Inline styles: 12 instances
   - No design system imports
   - **Fix:** Replace with tokens from STYLE_PICK

   ## Warnings
   ### [WARN] src/components/Card.tsx
   - Partial token usage (colors yes, spacing no)
   - **Fix:** Apply spacing scale

   ## Summary
   - Critical: N findings
   - Warning: N findings
   - Info: N findings
   ```

4. **Write `PRIORITY.md`:**
   ```
   # Fix Priority

   ## Wave 1: Tokens (easy, high impact)
   - src/styles/variables.css — replace hardcoded colors
   - src/styles/typography.css — align font scale

   ## Wave 2: Core Components (medium)
   - src/components/Button.tsx — token migration
   - src/components/Input.tsx — token migration

   ## Wave 3: Layout (medium)
   - src/components/Grid.tsx — spacing alignment

   ## Wave 4: Page Components (hard)
   - src/pages/Dashboard.tsx — full alignment
   ```
   - Rank by impact/effort ratio
   - Each wave = 10-15 files (simple), 5-10 files (medium), 3-5 files (hard)
   - Dependencies: tokens before components, components before layout

5. **Recommendation:** Review AUDIT.md and PRIORITY.md. Proceed with fixes or adjust plan.

## Phase 4: Fix (complexity-dependent)

**Simple mode (complexity < 50 files):**

Fix all waves. For each wave:
1. Apply changes to listed files
2. Replace hardcoded colors with CSS variables/tokens
3. Replace inline styles with classes
4. Replace px with rem/em where appropriate
5. Add missing ARIA labels
6. Verify: build passes, no new errors
7. Record progress in `PROGRESS.md`

**Medium mode (50-200 files):**

Fix Wave 1 (tokens) only:
1. Replace hardcoded colors with CSS variables
2. Align typography to design system scale
3. Align spacing to design system scale
4. Verify: build passes
5. Write `PROGRESS.md`
6. **Recommendation:** Run refactor for remaining changes:
   ```
   /gsd workflow refactor 'apply UI consistency fixes' --context .gsd/workflows/ui-consistency/YYYY-MM-DD/AUDIT.md
   ```

**Hard mode (>200 files):**

No code changes. STRICTLY NO FILE MODIFICATIONS.
1. Generate AUDIT.md with detailed findings
2. Generate PRIORITY.md with ranked list
3. **Recommendation:** Run refactor:
   ```
   /gsd workflow refactor 'apply UI consistency fixes' --context .gsd/workflows/ui-consistency/YYYY-MM-DD/AUDIT.md
   ```
4. If workflow attempts to modify files in hard mode → abort with error

**Git behavior:**
- Without `--create-branch`: Workflow modifies files but does NOT commit. GSD/user manages git.
- With `--create-branch`: Create branch `ui-consistency/YYYY-MM-DD`, each wave = atomic commit. Blocked if uncommitted changes exist.

## Phase 5: Verify

**Goal:** Confirm fixes work, no new drift.

1. **Re-scan modified files:**
   ```bash
   # Re-classify fixed files
   for file in $(cat /tmp/modified-files.txt); do
     # Check if hardcoded colors remain
     grep -c '#[0-9a-fA-F]\{3,8\}' "$file"
     # Check if inline styles remain
     grep -c 'style={{' "$file"
   done
   ```

2. **Update `inventory.json`:**
   - Re-run classification heuristics on fixed files
   - Update classification: legacy → modern, drift → modern
   - Update lastScan timestamp

3. **Write `UI_VERIFY.json`:**
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
       { "path": "/", "status": "pass" }
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
       "colorConsistency": { "status": "pass", "evidence": "0 hardcoded colors found in scan" },
       "spacingScale": { "status": "pass", "evidence": "All spacing values align with design system" }
     },
     "nextSteps": []
   }
   ```
   Save to `.gsd/ui-gates/UI_VERIFY.json`

4. **Browser verification** (if web app running):
   - Navigate to key pages
   - Screenshot before/after
   - Check visual consistency
   - Use `ui_ux_browser_plan` + `ui_ux_browser_run` if available

5. **Write `BEFORE_AFTER.md`:**
   ```
   # Before/After Comparison

   Date: YYYY-MM-DD

   ## Colors
   Before: 15 hardcoded → After: 0 hardcoded

   ## Spacing
   Before: 23 inline px → After: all rem-based

   ## Components Fixed
   - Button.tsx: added design system imports
   - Card.tsx: replaced inline styles with classes
   - Input.tsx: aligned to spacing scale
   ```

6. **Update `METRICS.json`:**
   - Recount: modern/legacy/drift/unknown
   - Compare with pre-fix metrics
   - Calculate improvement percentage

7. **Recommendations:**
   - If new drift found: "Run workflow again: `/gsd workflow ui-consistency`"
   - If all clean: "UI consistency maintained. Next audit recommended after next UI milestone"
   - If metrics degraded: "Review BEFORE_AFTER.md and adjust fixes"

</process>

<outputs>
Each run produces artifacts in `.gsd/workflows/ui-consistency/YYYY-MM-DD/`:

| Phase | Artifact | Description |
|-------|----------|-------------|
| 0 | RESEARCH.md | Codebase analysis + user input |
| 1 | STYLE_PICK.md | Visual direction (in .gsd/ui-gates/) |
| 1 | DESIGN_DNA.md | Design personality (in .gsd/ui-gates/) |
| 1 | COMPONENT_PLAN.md | Component specs (in .gsd/ui-gates/) |
| 2 | INVENTORY.md | All UI files with classification |
| 2 | METRICS.json | Quantitative metrics |
| 2 | inventory.json | Classification registry (in .gsd/ui-gates/) |
| 3 | AUDIT.md | Detailed audit findings |
| 3 | PRIORITY.md | Ranked fix list |
| 4 | PROGRESS.md | Progress per wave (if fixes applied) |
| 5 | BEFORE_AFTER.md | Comparison report |
| 5 | UI_VERIFY.json | Verification evidence (in .gsd/ui-gates/) |
| 5 | METRICS.json | Updated metrics (post-fix) |
</outputs>

<integration>
**ui-gates tools** (if available):
- `ui_ux_source_scan` → Phase 2 (SCAN)
- `ui_ux_validate_gate_pack` → Phase 3 (AUDIT)
- `ui_ux_structural_review` → Phase 3 (AUDIT)
- `ui_ux_optical_review` → Phase 3 (AUDIT)
- `ui_ux_browser_plan` → Phase 5 (VERIFY)
- `ui_ux_browser_run` → Phase 5 (VERIFY)

**GSD skills** (use if relevant):
- `frontend-design` → Phase 4 (FIX) — apply design patterns
- `make-interfaces-feel-better` → Phase 3 (AUDIT) — check polish
- `userinterface-wiki` → Phase 3 (AUDIT) — reference rules
- `web-design-guidelines` → Phase 3 (AUDIT) — check compliance
- `accessibility` → Phase 3 (AUDIT) — WCAG check
- `core-web-vitals` → Phase 5 (VERIFY) — performance

**Auto-mode integration:**
- Skill `ui-consistency` loaded for UI tasks
- `pre_dispatch_hooks` inject STYLE_PICK reference in task plans
- `custom_instructions` remind LLM about design system
</integration>

<safety>
**Hard mode guard:** If complexity = hard and workflow attempts to modify source files → abort with error message.

**Dirty working tree:** Without `--create-branch`, warn if uncommitted changes exist before fix phase. With `--create-branch`, block if uncommitted changes.

**Rollback:**
- Without `--create-branch`: `git checkout .` or `git stash`
- With `--create-branch`: `git checkout main` (abandon branch)
- After commit: `git revert <commit-hash>`
</safety>
