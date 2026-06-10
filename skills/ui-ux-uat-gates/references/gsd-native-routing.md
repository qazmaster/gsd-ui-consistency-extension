# GSD-native UI/UX gate routing

This skill is global but must remain native to GSD. It is a guard/gate layer, not a replacement router.

## Skill routing

Use exactly one primary skill where possible and at most one guard skill.

| Trigger | Primary skill | Guard |
|---|---|---|
| Build page/component/dashboard/landing UI | `frontend-design` | `verify-before-complete` |
| Polish hover states, typography, borders, spacing, motion | `make-interfaces-feel-better` | `verify-before-complete` |
| Premium critique, expensive feel, less generic output | `premium-ux-review` | `verify-before-complete` |
| WCAG, keyboard, screen reader, labels, focus | `accessibility` | `verify-before-complete` |
| LCP, CLS, INP, page-experience | `core-web-vitals` | `verify-before-complete` |
| React/Next UI performance and rendering patterns | `react-best-practices` | `verify-before-complete` |
| Auth/payment/PII/external data in UI | `security-review` | `verify-before-complete` |

## Lifecycle hooks as agent behavior

These are not kernel hooks. They are workflow checkpoints.

### on_plan_task

If UI-impacting, add a UI Verification Contract to the task plan:

- Surface
- Routes
- Viewports
- STYLE_PICK required
- DESIGN_DNA required
- COMPONENT_PLAN required
- Browser UAT required
- Accessibility smoke required

### before_edit_ui_file

- Confirm STYLE_PICK exists or create it.
- Confirm COMPONENT_PLAN exists if adding components/libraries/runtime.
- Check package dependency before import.
- Reject forbidden motion runtime for the surface unless explicitly justified.

### after_edit_ui_file

Run lightweight checks:

- no placeholder/TODO/rest-of-code
- no canonical purple-blue AI gradient unless explicitly justified
- no `transition: all`
- no width/height/top/left animation for ordinary UI
- no missing reduced-motion path for nontrivial motion
- no focus outline removal without focus-visible replacement
- no commercial stock URLs without license evidence
- no default ShadCN aesthetic when customization was claimed
- no Magic UI demo reel
- no motion stack conflict

### before_task_complete

- Run code verification.
- Run browser UAT.
- Save UI_VERIFY.
- Validate gate pack.
- Include artifact paths in task completion evidence.

### before_slice_complete

- Aggregate task UI_VERIFY artifacts into slice UAT.
- Confirm STYLE_PICK/DESIGN_DNA coherence across tasks.
- Record limitations/follow-ups for warnings.
