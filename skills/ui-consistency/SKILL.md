---
name: ui-consistency
description: >
  Maintain UI/UX consistency across a project via design system generation, drift detection,
  and wave-based remediation. Integrates with GSD auto-mode through STYLE_PICK/DESIGN_DNA
  awareness. Use when asked to "check UI consistency", "audit design system", "fix UI drift",
  "generate design system", "run ui-consistency", or when working on UI components without
  existing design system references.
---

<objective>
Ensure visual and behavioral consistency across all UI components in a project. This skill
provides three capabilities:

1. **Design system generation** — create STYLE_PICK.md, DESIGN_DNA.md, COMPONENT_PLAN.md from
   existing codebase analysis + user input
2. **Drift detection** — scan UI files, classify as modern/legacy/drift, produce AUDIT.md with
   prioritized findings
3. **Wave-based remediation** — fix inconsistencies in ordered waves (tokens first, then
   components, then layout) with verification between each

The skill operates in three complexity modes: **simple** (inline fixes, <50 components),
**medium** (token fixes only, rest via refactor), **hard** (audit-only, no code changes).

**Phases:**
0. **Research** — analyze codebase + ask user design questions
1. **Generate** — create STYLE_PICK.md, DESIGN_DNA.md, COMPONENT_PLAN.md
2. **Scan** — find all UI files, classify, count metrics
3. **Audit** — check each file against design system, prioritize findings
4. **Fix** — apply fixes (complexity-dependent) or generate AUDIT.md
5. **Verify** — re-scan, browser screenshots, before/after comparison
</objective>

<essential_principles>

<principle name="design-system-is-truth">
STYLE_PICK.md, DESIGN_DNA.md, COMPONENT_PLAN.md in `.gsd/ui-gates/` are the single source of
truth. All UI work must reference them. If they don't exist, generate them first (Phase 0-1).
</principle>

<principle name="complexity-determines-mode">
Never guess the mode. Assess complexity automatically (file count, CSS approach, component
variants) then choose: simple → fix all, medium → fix tokens + audit rest, hard → audit only.
</principle>

<principle name="advisory-not-blocking">
This skill is advisory by default. It warns about drift but never blocks task completion.
Escalation to "block" requires explicit user configuration.
</principle>

<principle name="legacy-is-inventory">
Legacy components are not broken — they're tracked. Enforcement applies only to modern
components. Migrate legacy on touch, not in bulk.
</principle>

</essential_principles>

<auto_mode_integration>

GSD auto-mode integration via stable extension points:

1. **Skill routing** (Layer A): This skill loads automatically for UI tasks via `skill_rules` in PREFERENCES.md
2. **Custom instructions** (Layer B): `custom_instructions` contain design system awareness reminder
3. **Pre-dispatch hook** (Layer C): `pre_dispatch_hooks` inject STYLE_PICK reference into task plans:
   ```yaml
   pre_dispatch_hooks:
     - name: ui-consistency-hint
       before: [execute-task, plan-slice]
       action: modify
       prepend: "Check STYLE_PICK at .gsd/ui-gates/STYLE_PICK.md before modifying UI components."
   ```

When the hook fires, the executor sees STYLE_PICK reference in the task plan and follows
its color palette, typography, spacing, and component specs.

**Deprecated workflow template:**
The old `ui-consistency` workflow template (`/gsd start ui-consistency`) is deprecated.
Use this skill directly — mention "check UI consistency" or "audit design system" and
routing will activate automatically. The template is kept for backward compatibility only.

**Implemented layers:** A, B, C (fully working).

**NOT implemented (documented for future enhancement):**
- Prompt injection into system prompt (requires GSD core support for dynamic injection)
- Completion enforcement (requires GSD core support for UI-aware completion gates)
- Auto-audit after milestone (manual trigger only for MVP)

</auto_mode_integration>

<routing>

Based on user intent, route to the appropriate workflow:

**Generate design system from scratch:**
→ workflows/generate-design-system.md

**Audit existing codebase for drift:**
→ workflows/audit-and-fix.md

**Quick scan without fix:**
→ workflows/quick-scan.md

**Fix phase only (audit already exists):**
→ workflows/fix-only.md

**Check if design system exists and is current:**
→ Run: `ls .gsd/ui-gates/STYLE_PICK.md .gsd/ui-gates/DESIGN_DNA.md .gsd/ui-gates/COMPONENT_PLAN.md 2>/dev/null`
→ If missing: route to generate-design-system
→ If present: route to audit-and-fix

**Unclear intent:**
→ Ask: "Do you want to (A) generate a design system, (B) audit for drift, or (C) fix known issues?"

</routing>

<reference_index>

**Complexity detection:** references/complexity-detection.md
**Legacy classification:** references/legacy-classification.md
**Wave planning:** references/wave-planning.md
**Design system format:** references/design-system-format.md
**Token inheritance:** references/token-inheritance.md

</reference_index>

<workflows_index>

| Workflow | Purpose |
|----------|---------|
| generate-design-system.md | Create STYLE_PICK + DESIGN_DNA + COMPONENT_PLAN from codebase |
| audit-and-fix.md | Full pipeline: scan → audit → fix → verify |
| quick-scan.md | Scan + audit only, no code changes |
| fix-only.md | Apply fixes from existing AUDIT.md |

</workflows_index>

<quick_start>

**First run (no design system):**
```bash
# 1. Generate design system
# Load workflows/generate-design-system.md and follow Phase 0-1

# 2. Run audit
# Load workflows/audit-and-fix.md and follow Phase 2-3

# 3. Apply fixes (if complexity allows)
# Load workflows/fix-only.md
```

**Subsequent runs (design system exists):**
```bash
# Full audit + fix pipeline
# Load workflows/audit-and-fix.md
```

**Artifacts location:**
- Design system: `.gsd/ui-gates/` (STYLE_PICK.md, DESIGN_DNA.md, COMPONENT_PLAN.md)
- Audit results: `.gsd/ui-gates/` (AUDIT.md, PRIORITY.md, INVENTORY.md, UI_VERIFY.json)
- Legacy location (deprecated): `.gsd/workflows/ui-consistency/YYYY-MM-DD/` — migrate to unified dir

**Command reference:**
| Command | Effect |
|---------|--------|
| `--audit-only` | Force hard mode (audit only, no code changes) |
| `--fix` | Force simple mode (fix all, ignore complexity) |
| `--fix-tokens` | Force medium mode (fix tokens only) |
| `--classify=path=class` | Manual override: modern/legacy/drift |

</quick_start>

<success_criteria>

Design system exists and is referenced:
- `.gsd/ui-gates/STYLE_PICK.md` contains visual direction
- `.gsd/ui-gates/DESIGN_DNA.md` contains personality/density/trust specs
- `.gsd/ui-gates/COMPONENT_PLAN.md` contains component shell/states/verification

Audit completed:
- All UI files classified (modern/legacy/drift)
- AUDIT.md lists findings with severity and effort
- PRIORITY.md ranks fixes by impact/effort ratio

Fixes applied (simple/medium mode):
- Each wave verified independently
- No new drift introduced
- BEFORE_AFTER.md documents changes

</success_criteria>

<implementation_status>

| Phase | Status | Description |
|-------|--------|-------------|
| A | ✅ | Skill structure — SKILL.md, workflows, references, routing |
| B | ✅ | Routing — skill_rules, hooks, PREFERENCES.md, SKILL-ROUTING.md |
| C | ✅ | Workflow template — markdown-phase, 6 phases, complexity modes |
| D | ✅ | UI_VERIFY.json — proper schema, validated, reference docs |
| E | ✅ | Inventory.json — 98 files classified, schema docs, --classify flag |
| F | ✅ | Token inheritance — designSystem.base config, merge logic, reference |
| G | ✅ | Documentation — SKILL.md, references, workflow templates |

</implementation_status>
