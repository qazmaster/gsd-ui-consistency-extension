# Workflow: Fix Only

<required_reading>
- references/wave-planning.md
</required_reading>

<purpose>
Apply fixes from an existing AUDIT.md. Use when audit is already complete and you only need
to execute the fix plan. Requires AUDIT.md and PRIORITY.md to exist.
</purpose>

<process>

1. **Verify prerequisites:**
   ```bash
   # Find latest audit
   ls -t .gsd/workflows/ui-consistency/*/AUDIT.md | head -1
   ls -t .gsd/workflows/ui-consistency/*/PRIORITY.md | head -1
   ```
   If missing → run audit-and-fix workflow first.

2. **Read PRIORITY.md** to understand wave structure.

3. **Read AUDIT.md** for specific findings per file.

4. **For each wave in PRIORITY.md:**
   - Apply changes to listed files
   - Verify (build passes, no new errors)
   - Record progress in PROGRESS.md:
     ```
     ## Wave 1: Tokens
     - [x] src/styles/variables.css — replaced 15 hardcoded colors
     - [x] src/styles/typography.css — aligned font scale
     - Status: COMPLETE
     
     ## Wave 2: Core Components
     - [ ] src/components/Button.tsx — pending
     ```

5. **After all waves:**
   - Re-scan modified files
   - Report: "N files fixed, M remaining issues"

6. **If scope flag provided** (`--scope=components/Button`):
   - Fix only files matching scope
   - Skip other waves

7. **If from-wave flag provided** (`--from-wave=3`):
   - Skip waves 1-2
   - Start from wave 3

</process>

<success_criteria>
- All waves in PRIORITY.md processed
- PROGRESS.md tracks completion per wave
- Build passes after each wave
- No new drift introduced
</success_criteria>
