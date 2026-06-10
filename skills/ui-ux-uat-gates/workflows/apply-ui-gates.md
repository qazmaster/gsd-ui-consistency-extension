# Workflow: Apply UI/UX UAT Gates

<required_reading>
Read these reference files now:

1. `references/gsd-native-routing.md`
2. `references/gate-policy.md`
3. `references/detent-mapping.md`
</required_reading>

<process>
## Step 1: Classify UI impact

Treat a task as UI-impacting if it changes pages, routes, components, CSS, design tokens, animation/motion, copy layout, forms, navigation, frontend data display, responsive behavior, browser-visible states, or public-web performance.

If not UI-impacting, record “UI gates not applicable” in the normal GSD verification summary and stop.

## Step 2: Choose native GSD skill routing

Select the primary skill using GSD’s existing policy. Use this skill as the guard/gate layer.

- Build page/component/dashboard/landing UI → `frontend-design`
- Polish interactions/spacing/motion/typography → `make-interfaces-feel-better`
- Premium critique or “looks generic” → `premium-ux-review`
- WCAG/a11y/keyboard/screen reader → `accessibility`
- LCP/CLS/INP/page-experience → `core-web-vitals`
- React/Next UI patterns → `react-best-practices`
- Completion claim → `verify-before-complete`

## Step 3: Create or update STYLE_PICK

Copy `templates/STYLE_PICK.md` into the active task/slice artifact directory. Commit one style direction. If the project already has a design system, use `project-native` and document inherited constraints.

Fail closed when STYLE_PICK is missing for a UI task that changes visual direction.

## Step 4: Create or update DESIGN_DNA

Copy `templates/DESIGN_DNA.md`. Persist the slice’s visual language, motion stance, density, accessibility posture, signature move, and component hints.

For multi-task UI slices, keep DESIGN_DNA stable unless a user-approved redesign changes it.

## Step 5: Create or update COMPONENT_PLAN

Copy `templates/COMPONENT_PLAN.md`. Record components, existing primitives to reuse, external library tracks, motion runtime decision, interaction state coverage, dropped patterns, and UAT implications.

Block risky runtime choices unless explicitly justified:

- GSAP is blocked on dashboards/app-shell/docs/settings/internal tools unless cinematic motion is explicitly requested.
- Lenis is never-fire on utilitarian surfaces.
- Magic UI ambience is restricted on dashboards/app-shell/docs/settings.
- Do not mix GSAP/ThreeJS with Framer Motion in the same component tree.

## Step 6: Implement and run code verification

Use normal project verification: build, typecheck, lint, tests, and LSP diagnostics as appropriate. Do not treat compile success as UI success.

## Step 7: Run browser UAT

Use a real local app when possible:

1. Start server with `bg_shell start` and `wait_for_ready`.
2. Navigate with browser tools.
3. Verify required routes.
4. Test desktop/tablet/mobile viewports.
5. Assert primary content and actions are visible.
6. Check console and network failures.
7. Check horizontal scroll, focus visibility, and key interactions.
8. Capture screenshots or debug bundles when meaningful.

## Step 8: Fill UI_VERIFY

Copy `templates/UI_VERIFY.md`. Record commands, browser actions, evidence paths, verdicts, limitations, and follow-ups.

Overall verdict rules:

- `PASS`: no blockers and evidence is present.
- `NEEDS_ATTENTION`: no blockers, but warnings or skipped checks require documented follow-up.
- `FAIL`: any blocker or missing required evidence.

## Step 9: Validate gate pack

Run:

```bash
python3 ~/.agents/skills/ui-ux-uat-gates/scripts/validate-ui-gate-pack.py <artifact-dir> --json
```

If it fails, fix missing artifacts/evidence or report the UI task as not complete. Do not claim “done”.

## Step 10: Complete through normal GSD channels

When verification passes, reference the artifact paths and validator output in `gsd_task_complete` / `gsd_slice_complete` verification fields. Do not manually toggle GSD checkboxes.
</process>

<success_criteria>
This workflow is complete when:

- UI impact was classified correctly
- Existing GSD skill routing was preserved
- STYLE_PICK, DESIGN_DNA, COMPONENT_PLAN, and UI_VERIFY exist or are explicitly not applicable
- Browser UAT evidence is fresh and inspectable
- The validator passes or the non-PASS verdict is reported honestly
- Completion claims include evidence, not taste-only prose
</success_criteria>
