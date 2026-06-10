# UI/UX UAT gate policy

## Verdicts

- `PASS`: required evidence exists and no blockers remain.
- `NEEDS_ATTENTION`: no blockers, but warnings/skipped checks need documented limitation or follow-up.
- `FAIL`: blocker exists or required evidence is missing/stale.

## Blockers

Block completion claims:

- route fails to load
- blank page/canvas where content is expected
- console error affecting behavior
- failed critical fetch/XHR
- horizontal overflow on required viewport
- primary CTA/form/path unusable
- keyboard focus invisible or primary path unreachable where relevant
- missing required UI_VERIFY evidence
- forbidden motion runtime for surface
- placeholder/TODO/rest-of-code shipped
- commercial-stock asset without explicit license evidence
- unresolved accessibility blocker for task scope

## Warnings

Allow completion only with documented limitation/follow-up:

- STYLE_PICK confidence medium/low
- visual signature too generic
- minor responsive polish issue with workaround
- non-critical network request failed
- subjective premium/polish concern
- expected visual diff but no baseline
- skipped screenshot with credible reason

## Notes

Informational:

- optional evidence skipped with reason
- future enhancement outside scope
- minor copy improvement

## Evidence minimum

For UI tasks that render in a browser:

- route list
- desktop, tablet, mobile viewport checks
- screenshot path or explicit screenshot unavailable reason
- console error status
- failed network request status
- horizontal scroll status
- focus visibility status
- primary flow status
- accessibility smoke status
- overall verdict

If the app cannot be run locally, UI_VERIFY must record why and downgrade to `NEEDS_ATTENTION` or `FAIL` depending on risk. Do not mark PASS without browser evidence unless the task is a non-rendering design artifact.

## Auto-mode safety

- Do not patch auto-mode internals.
- Do not write directly to `.gsd/runtime`, `.gsd/activity`, or `.gsd/gsd.db`.
- Use `gsd_*` tools for GSD state transitions.
- Use browser tools for UI evidence.
- Use project-local or global skills for guidance.
- Fail closed on missing evidence.
