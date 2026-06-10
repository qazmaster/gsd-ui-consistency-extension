# Workflow: Audit and Fix UI Consistency

<required_reading>
- references/complexity-detection.md
- references/legacy-classification.md
- references/wave-planning.md
</required_reading>

<purpose>
Full pipeline: scan UI files, classify components, audit against design system, produce
prioritized fix plan, and optionally apply fixes in waves. Complexity determines mode.
</purpose>

<process>

## Phase 2: Scan

**Goal:** Find all UI files and classify them.

1. **Verify design system exists:**
   ```bash
   ls .gsd/ui-gates/STYLE_PICK.md .gsd/ui-gates/DESIGN_DNA.md .gsd/ui-gates/COMPONENT_PLAN.md
   ```
   If missing → run generate-design-system workflow first.

2. **Find all UI files:**
   ```bash
   find src -name "*.tsx" -o -name "*.jsx" -o -name "*.vue" -o -name "*.svelte" \
     -o -name "*.css" -o -name "*.scss" -o -name "*.module.css" -o -name "*.html" \
     | sort > /tmp/ui-files.txt
   wc -l /tmp/ui-files.txt
   ```

3. **Assess complexity** (see references/complexity-detection.md):
   - Count total UI files
   - Check CSS approach (Tailwind/CSS vars/CSS-in-JS/inline)
   - Count component variants
   - Determine: simple / medium / hard

4. **Classify each file** (see references/legacy-classification.md):
   - **modern:** uses design tokens, imports from design system, follows STYLE_PICK
   - **legacy:** hardcoded colors, inline styles, old patterns, no design system imports
   - **drift:** mixed patterns (partial tokens + partial hardcoded)

5. **Produce INVENTORY.md:**
   ```
   # UI File Inventory

   Generated: YYYY-MM-DD
   Total files: N
   Complexity: simple|medium|hard

   ## Classification Summary
   - Modern: N files (X%)
   - Legacy: N files (X%)
   - Drift: N files (X%)

   ## File List
   | File | Classification | Reason |
   |------|---------------|--------|
   | src/components/Button.tsx | modern | uses tokens, follows STYLE_PICK |
   | src/components/OldModal.tsx | legacy | inline styles, hardcoded #fff |
   ```

6. **Produce METRICS.json:**
   ```json
   {
     "totalFiles": 45,
     "modern": 30,
     "legacy": 10,
     "drift": 5,
     "complexity": "simple",
     "cssApproach": "tailwind",
     "componentCount": 25,
     "variantCount": 3.2
   }
   ```

## Phase 3: Audit

**Goal:** Check each file against design system, find anti-patterns.

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

3. **Produce AUDIT.md:**
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

4. **Produce PRIORITY.md:**
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

## Phase 4: Fix (complexity-dependent)

**Simple mode (complexity < 50 files):**

Fix all waves. For each wave:
1. Apply changes
2. Verify (build passes, no new errors)
3. Note progress in PROGRESS.md

**Medium mode (50-200 files):**

Fix Wave 1 (tokens) only:
1. Apply token changes
2. Verify
3. Recommend: run refactor workflow for remaining changes
   ```
   /gsd workflow refactor 'apply UI consistency fixes' --context .gsd/ui-gates/AUDIT.md
   ```

**Hard mode (>200 files):**

No code changes. Generate AUDIT.md + PRIORITY.md only.
Recommend:
```
/gsd workflow refactor 'apply UI consistency fixes' --context .gsd/ui-gates/AUDIT.md
```

## Phase 5: Verify

**Goal:** Confirm fixes work, no new drift.

1. **Re-scan** modified files
2. **Browser verification** (if web app):
   - Screenshot before/after
   - Check visual consistency
3. **Produce BEFORE_AFTER.md:**
   ```
   # Before/After Comparison

   ## Colors
   Before: 15 hardcoded → After: 0 hardcoded

   ## Spacing
   Before: 23 inline px → After: all rem-based
   ```

4. **Recommendations:**
   - If new drift found: "Run workflow again"
   - If all clean: "UI consistency maintained. Next audit after next UI milestone"

</process>

<success_criteria>
- All UI files classified in INVENTORY.md
- AUDIT.md lists all findings with severity
- PRIORITY.md ranks fixes by wave
- Simple/medium: fixes applied and verified
- Hard: AUDIT.md + PRIORITY.md ready for refactor workflow
- BEFORE_AFTER.md documents changes (if fixes applied)
</success_criteria>
