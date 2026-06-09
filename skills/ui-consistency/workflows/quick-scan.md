# Workflow: Quick Scan

<required_reading>
- references/complexity-detection.md
- references/legacy-classification.md
</required_reading>

<purpose>
Scan UI files and produce audit findings without applying any fixes. Lightweight alternative
to full audit-and-fix. Use when you want to check drift status without committing to changes.
</purpose>

<process>

1. **Verify design system exists:**
   ```bash
   ls .gsd/ui-gates/STYLE_PICK.md .gsd/ui-gates/DESIGN_DNA.md .gsd/ui-gates/COMPONENT_PLAN.md
   ```

2. **Find and count UI files:**
   ```bash
   find src -name "*.tsx" -o -name "*.jsx" -o -name "*.vue" -o -name "*.css" -o -name "*.scss" | wc -l
   ```

3. **Classify files** (see references/legacy-classification.md):
   - Sample 10-15 representative files
   - Apply heuristics (hardcoded colors, inline styles, token usage)
   - Extrapolate classification percentages

4. **Check for top anti-patterns:**
   - Hardcoded colors: `grep -rn '#[0-9a-fA-F]\{3,8\}' src/ --include="*.tsx" --include="*.css" | wc -l`
   - Inline styles: `grep -rn 'style={{' src/ --include="*.tsx" | wc -l`
   - Missing ARIA: `grep -rL 'aria-\|role=' src/ --include="*.tsx" | head -10`

5. **Produce summary** (stdout, no files):
   ```
   UI Consistency Quick Scan
   ========================
   Files: 45 total (30 modern, 10 legacy, 5 drift)
   Complexity: simple
   
   Top issues:
   - 23 hardcoded color instances across 8 files
   - 12 inline style instances across 4 files
   - 5 components missing ARIA labels
   
   Recommendation: Run full audit (/gsd workflow ui-consistency)
   ```

</process>

<success_criteria>
- Classification percentages reported
- Top 3-5 anti-patterns identified with counts
- Complexity level determined
- Recommendation provided (full audit, generate design system, or no action needed)
</success_criteria>
