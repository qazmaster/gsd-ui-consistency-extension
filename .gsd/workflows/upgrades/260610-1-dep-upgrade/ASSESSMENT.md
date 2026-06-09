# Dependency Upgrade Assessment

**Project:** pi-extension-ui-consistency (GSD UI Consistency Extension)  
**Date:** 2026-06-09  
**Branch:** `gsd/dep-upgrade/dep-upgrade`  
**Assessor:** executor-01

---

## 1. Inventory

### Project Type
- Node.js (ES module) TypeScript extension for GSD/pi
- No `dependencies` block in `package.json`
- Runtime surface is provided via `peerDependencies` only
- Validation is Python-based (`skills/ui-consistency/tests/*.py`)
- No lockfile (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`) present
- No `node_modules` installed

### Outdated Dependencies
```
$ npm outdated
(no output)
```

`npm outdated` reports nothing because the project has no installed `node_modules` and no lockfile. All declared dependencies are `peerDependencies` with wildcard (`*`) versions:

| Package | Current Declared | Type | Notes |
|---|---|---|---|
| `@gsd/pi-ai` | `*` | peer | Internal GSD package |
| `@gsd/pi-coding-agent` | `*` | peer | Internal GSD package |
| `@gsd/pi-tui` | `*` | peer | Internal GSD package |
| `@sinclair/typebox` | `*` | peer | External JSON-schema library |

### Security Audit
```
$ npm audit
This command requires an existing lockfile.
```
No lockfile means `npm audit` cannot run. There are no direct runtime dependencies to audit.

### Runtime / Tooling Versions
- Node.js: v25.9.0
- npm: 11.12.1
- Python: used only for validation tests (CI runs `python3 run_all_tests.py`)

---

## 2. Impact Analysis

### `@sinclair/typebox`
- **Blast radius:** `index.ts` imports `Type` from `@sinclair/typebox` and uses `Type.Object`, `Type.String`, `Type.Optional`, etc.
- **Risk:** The wildcard peer dep means consumers can install any version. Typebox has had breaking changes between major versions (e.g., v0.31 → v0.32 changed some API shapes and Value.* behavior).
- **Current code check:** `index.ts` uses only stable `Type.*` constructors (`Type.Object`, `Type.String`, `Type.Optional`, `Type.Boolean`) and does not use `Value.*` or compiler APIs, so most minor/patch bumps are safe.

### `@gsd/pi-ai`, `@gsd/pi-coding-agent`, `@gsd/pi-tui`
- **Blast radius:** Extension API surface (`ExtensionAPI`, `StringEnum`) and hook signatures.
- **Risk:** Internal GSD packages; versions are controlled by the host (pi/GSD). Wildcard is correct for an extension that ships inside the GSD agent runtime.
- **No action needed** — these are intentionally peer deps.

### GitHub Actions CI
- `actions/checkout@v4` and `actions/setup-python@v5` are current stable versions.
- No outdated Actions detected.

---

## 3. Risk Classification

| Item | Bump Kind | Risk | Decision |
|---|---|---|---|
| `@sinclair/typebox` peer dep | unknown (wildcard) | Medium | Pin to a minimum safe version to avoid consumer drift |
| `@gsd/pi-ai` peer dep | none | Low | Keep wildcard (host-provided) |
| `@gsd/pi-coding-agent` peer dep | none | Low | Keep wildcard (host-provided) |
| `@gsd/pi-tui` peer dep | none | Low | Keep wildcard (host-provided) |
| Add `package-lock.json` / lockfile | N/A | Low | Recommended for reproducible installs and audit support |

---

## 4. Recommended Upgrade Scope

Because this project has **no installed dependencies and no lockfile**, the practical upgrade work is:

1. **Pin `@sinclair/typebox` peer dependency** from `*` to a known-stable minimum version (e.g., `^0.34.0` or the latest stable at time of upgrade). This prevents consumers from silently installing a future major that breaks the extension.
2. **Generate a `package-lock.json`** so that:
   - `npm audit` can run in CI/local dev.
   - Reproducible installs are possible.
   - Future `npm outdated` has a baseline to compare against.
3. **Verify** the existing Python test suite still passes.
4. **Verify** `install.sh` still works end-to-end.

No runtime dependency upgrades are available because there are no runtime dependencies.

---

## 5. Upgrade Order

1. **Batch 1 — Tooling baseline**
   - Add `package-lock.json` via `npm install --package-lock-only` (or full install if peer deps resolvable).
   - If GSD internal packages are not resolvable from npm, document that and skip lockfile generation for those peers.

2. **Batch 2 — Peer dependency guardrails**
   - Update `package.json` to pin `@sinclair/typebox` to a minimum stable version.
   - Keep `@gsd/*` packages as `*` (host contract).

3. **Batch 3 — Verification**
   - Run Python validation tests.
   - Run install script smoke test.
   - Confirm no regressions.

---

## 6. Deferred / Out of Scope

- Major version upgrades to `@sinclair/typebox` beyond the pinned minimum — will be handled when a specific consumer need or security advisory arises.
- Bumping Node.js `engines` field — currently `>=20`; no need to change unless CI or host requires it.
- Adding runtime `dependencies` — not required for this extension package.

---

## 7. Decision Gate

**Question:** Should we proceed with the recommended scope?

- **Option A (Recommended):** Pin `@sinclair/typebox` to a stable minimum version and generate a `package-lock.json` baseline. Verify tests pass.
- **Option B:** Do only the `package-lock.json` baseline without changing peer dep ranges.
- **Option C:** Close the workflow as "no actionable outdated dependencies" and document the state.
