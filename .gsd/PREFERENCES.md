---
version: 1
mode: solo

# UI Consistency Extension — Project Preferences
# Merged with global ~/.gsd/PREFERENCES.md

uiConsistency:
  workflow:
    defaultMode: auto
    complexityThreshold:
      simpleMaxFiles: 50
      mediumMaxFiles: 200
  designSystem:
    path: .gsd/ui-gates/
    autoGenerate: true
    base: ""  # Optional: path to shared design tokens (e.g. ~/.gsd/shared-design/tokens/)

pre_dispatch_hooks:
  - name: ui-consistency-hint
    before:
      - execute-task
      - plan-slice
    action: modify
    prepend: "Check STYLE_PICK at .gsd/ui-gates/STYLE_PICK.md before modifying UI components. If it exists, follow its color palette, typography, spacing, and component specs."

# Inherit from global:
# - models
# - skill_discovery
# - auto_supervisor
# - git settings
# - notifications
# - etc.
---

# GSD Skill Preferences

See `~/.gsd/agent/extensions/gsd/docs/preferences-reference.md` for full field documentation and examples.
See `~/.gsd/SKILL-ROUTING.md` for full skill routing policy, conflict matrix, and decision tree.
