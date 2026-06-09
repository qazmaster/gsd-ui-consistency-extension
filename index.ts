import type { ExtensionAPI } from "@gsd/pi-coding-agent";
import { Type } from "@sinclair/typebox";
import { StringEnum } from "@gsd/pi-ai";
import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";

// ─── Constants ──────────────────────────────────────────────────────────────

/** Directory where generated design system documents are stored. */
const DESIGN_SYSTEM_DIR = ".gsd/ui-gates";

/** Path to the STYLE_PICK.md design system document. */
const STYLE_PICK_PATH = join(DESIGN_SYSTEM_DIR, "STYLE_PICK.md");

/** Path to the DESIGN_DNA.md design system document. */
const DESIGN_DNA_PATH = join(DESIGN_SYSTEM_DIR, "DESIGN_DNA.md");

/** Path to the COMPONENT_PLAN.md design system document. */
const COMPONENT_PLAN_PATH = join(DESIGN_SYSTEM_DIR, "COMPONENT_PLAN.md");

// ─── Helper: check if design system exists ──────────────────────────────────

/**
 * Check whether all three design system documents exist in the workspace.
 * @param cwd - Workspace root directory.
 * @returns True when STYLE_PICK.md, DESIGN_DNA.md, and COMPONENT_PLAN.md all exist.
 */
function hasDesignSystem(cwd: string): boolean {
  return (
    existsSync(join(cwd, STYLE_PICK_PATH)) &&
    existsSync(join(cwd, DESIGN_DNA_PATH)) &&
    existsSync(join(cwd, COMPONENT_PLAN_PATH))
  );
}

// ─── Helper: read design system content ─────────────────────────────────────

/**
 * Read the contents of the design system documents.
 * @param cwd - Workspace root directory.
 * @returns Object containing the three design system documents, or null if reading fails.
 */
function readDesignSystem(cwd: string): { stylePick: string; designDna: string; componentPlan: string } | null {
  try {
    return {
      stylePick: readFileSync(join(cwd, STYLE_PICK_PATH), "utf-8"),
      designDna: readFileSync(join(cwd, DESIGN_DNA_PATH), "utf-8"),
      componentPlan: readFileSync(join(cwd, COMPONENT_PLAN_PATH), "utf-8"),
    };
  } catch {
    return null;
  }
}

// ─── Helper: classify UI files ──────────────────────────────────────────────

/** Classification result for a single UI file. */
interface FileClassification {
  path: string;
  classification: "modern" | "legacy" | "drift" | "unknown";
  reason: string;
}

/**
 * Classify a UI file's source content using heuristic pattern matching.
 * @param content - File source content.
 * @returns Classification label and a short reason.
 */
function classifyFile(content: string): { classification: FileClassification["classification"]; reason: string } {
  const hasHardcodedColors = /#[0-9a-fA-F]{3,8}\b|rgb\(a?\s*\([^)]*\)/.test(content);
  const hasInlineStyles = /style\s*=\s*\{\{/.test(content);
  const hasCssVariables = /var\s*\(/.test(content);
  const hasDesignSystemImports = /from\s+['"]\.\/design-system|from\s+['"]@theme|from\s+['"]\.\/tokens/.test(content);

  if (hasDesignSystemImports && hasCssVariables && !hasHardcodedColors) {
    return { classification: "modern", reason: "uses tokens, follows design system" };
  }
  if (hasHardcodedColors || hasInlineStyles) {
    if (hasCssVariables || hasDesignSystemImports) {
      return { classification: "drift", reason: "mixed patterns (partial tokens + hardcoded)" };
    }
    return { classification: "legacy", reason: "hardcoded colors or inline styles" };
  }
  if (!hasHardcodedColors && !hasInlineStyles && !hasCssVariables && !hasDesignSystemImports) {
    return { classification: "unknown", reason: "no UI indicators" };
  }
  return { classification: "drift", reason: "ambiguous patterns" };
}

// ─── Tool: ui_consistency_scan ──────────────────────────────────────────────

/**
 * Register the `ui_consistency_scan` tool that classifies UI files in a project.
 * @param pi - Extension API used to register the tool.
 */
function registerScanTool(pi: ExtensionAPI) {
  pi.registerTool({
    name: "ui_consistency_scan",
    label: "UI Consistency Scan",
    description: "Scan UI files and classify them as modern, legacy, drift, or unknown",
    promptSnippet: "Scan project UI files for consistency classification",
    parameters: Type.Object({
      scope: Type.Optional(Type.String({ description: "Directory or file path to scan (default: src/)" })),
    }),
    async execute(toolCallId, params, signal, onUpdate, ctx) {
      if (signal?.aborted) return { content: [{ type: "text", text: "Cancelled" }] };

      const scope = params.scope || "src";
      const cwd = ctx.cwd;

      onUpdate?.({
        content: [{ type: "text", text: `Scanning ${scope} for UI files...` }],
        details: { progress: 10 },
      });

      // Use bash to find files
      const { exec } = await import("node:child_process");
      const { promisify } = await import("node:util");
      const execAsync = promisify(exec);

      const extensions = ["tsx", "jsx", "vue", "svelte", "css", "scss", "module.css", "html"];
      const findCmd = `find ${scope} -type f \\( ${extensions.map(e => `-name "*.${e}"`).join(" -o ")} \\) 2>/dev/null | sort`;

      let files: string[] = [];
      try {
        const { stdout } = await execAsync(findCmd, { cwd, timeout: 30000 });
        files = stdout.trim().split("\n").filter(Boolean);
      } catch {
        return { content: [{ type: "text", text: `No UI files found in ${scope}` }] };
      }

      onUpdate?.({
        content: [{ type: "text", text: `Found ${files.length} UI files. Classifying...` }],
        details: { progress: 50 },
      });

      const classifications: FileClassification[] = [];
      let modern = 0, legacy = 0, drift = 0, unknown = 0;

      for (const file of files) {
        try {
          const content = readFileSync(join(cwd, file), "utf-8");
          const result = classifyFile(content);
          classifications.push({ path: file, classification: result.classification, reason: result.reason });
          switch (result.classification) {
            case "modern": modern++; break;
            case "legacy": legacy++; break;
            case "drift": drift++; break;
            case "unknown": unknown++; break;
          }
        } catch {
          classifications.push({ path: file, classification: "unknown", reason: "could not read" });
          unknown++;
        }
      }

      onUpdate?.({
        content: [{ type: "text", text: "Classification complete." }],
        details: { progress: 100 },
      });

      const total = files.length;
      const summary = [
        `# UI Consistency Scan Results`,
        ``,
        `**Scope:** ${scope}`,
        `**Total files:** ${total}`,
        ``,
        `## Summary`,
        `- Modern: ${modern} (${Math.round((modern / total) * 100)}%)`,
        `- Legacy: ${legacy} (${Math.round((legacy / total) * 100)}%)`,
        `- Drift: ${drift} (${Math.round((drift / total) * 100)}%)`,
        `- Unknown: ${unknown} (${Math.round((unknown / total) * 100)}%)`,
        ``,
        `## Classifications`,
        ...classifications.map(c => `- \`${c.classification}\` ${c.path} — ${c.reason}`),
      ].join("\n");

      return {
        content: [{ type: "text", text: summary }],
        details: {
          total,
          modern,
          legacy,
          drift,
          unknown,
          classifications,
          complexity: total < 50 ? "simple" : total < 200 ? "medium" : "hard",
        },
      };
    },
  });
}

// ─── Tool: ui_consistency_audit ─────────────────────────────────────────────

/**
 * Register the `ui_consistency_audit` tool that audits UI files against the design system.
 * @param pi - Extension API used to register the tool.
 */
function registerAuditTool(pi: ExtensionAPI) {
  pi.registerTool({
    name: "ui_consistency_audit",
    label: "UI Consistency Audit",
    description: "Audit UI files against the design system and report findings",
    promptSnippet: "Audit UI files for design system compliance",
    parameters: Type.Object({
      scope: Type.Optional(Type.String({ description: "Directory or file path to audit" })),
      mode: Type.Optional(StringEnum(["simple", "medium", "hard"] as const)),
    }),
    async execute(toolCallId, params, signal, onUpdate, ctx) {
      if (signal?.aborted) return { content: [{ type: "text", text: "Cancelled" }] };

      const cwd = ctx.cwd;

      if (!hasDesignSystem(cwd)) {
        return {
          content: [{ type: "text", text: "No design system found. Run `ui_consistency_generate_design_system` first." }],
          details: { error: "missing_design_system" },
        };
      }

      onUpdate?.({
        content: [{ type: "text", text: "Loading design system..." }],
        details: { progress: 10 },
      });

      const ds = readDesignSystem(cwd);
      if (!ds) {
        return {
          content: [{ type: "text", text: "Failed to read design system files." }],
          details: { error: "read_failed" },
        };
      }

      onUpdate?.({
        content: [{ type: "text", text: "Design system loaded. Running audit..." }],
        details: { progress: 30 },
      });

      // Run scan first
      const scanResult = await pi.exec("node", ["-e", `
        const fs = require('fs');
        const path = require('path');
        const scope = process.argv[1] || 'src';
        
        const extensions = ['tsx', 'jsx', 'vue', 'svelte', 'css', 'scss', 'module.css', 'html'];
        const files = [];
        
        function walk(dir) {
          try {
            const entries = fs.readdirSync(dir, { withFileTypes: true });
            for (const entry of entries) {
              const fullPath = path.join(dir, entry.name);
              if (entry.isDirectory() && entry.name !== 'node_modules') {
                walk(fullPath);
              } else if (entry.isFile()) {
                const ext = path.extname(entry.name).slice(1);
                if (extensions.includes(ext)) files.push(fullPath);
              }
            }
          } catch {}
        }
        
        walk(scope);
        console.log(JSON.stringify(files));
      `, params.scope || "src"], { cwd });

      let files: string[] = [];
      try {
        files = JSON.parse(scanResult.stdout);
      } catch {
        return { content: [{ type: "text", text: "Failed to scan files." }] };
      }

      onUpdate?.({
        content: [{ type: "text", text: `Auditing ${files.length} files...` }],
        details: { progress: 50 },
      });

      const findings: Array<{ file: string; severity: "critical" | "warning" | "info"; issue: string }> = [];

      for (const file of files) {
        try {
          const content = readFileSync(file, "utf-8");
          const relativePath = file.replace(cwd + "/", "");

          // Check for hardcoded colors
          const hardcodedColors = content.match(/#[0-9a-fA-F]{3,8}\b/g) || [];
          if (hardcodedColors.length > 0) {
            findings.push({
              file: relativePath,
              severity: "critical",
              issue: `Hardcoded colors: ${[...new Set(hardcodedColors)].slice(0, 5).join(", ")}${hardcodedColors.length > 5 ? "..." : ""}`,
            });
          }

          // Check for inline styles
          const inlineStyles = (content.match(/style\s*=\s*\{\{/g) || []).length;
          if (inlineStyles > 0) {
            findings.push({
              file: relativePath,
              severity: "warning",
              issue: `${inlineStyles} inline style instances`,
            });
          }

          // Check for px values (should use rem/em)
          const pxValues = (content.match(/\d+px/g) || []).length;
          if (pxValues > 5) {
            findings.push({
              file: relativePath,
              severity: "info",
              issue: `${pxValues} px values (consider rem/em)`,
            });
          }
        } catch {
          // Skip unreadable files
        }
      }

      onUpdate?.({
        content: [{ type: "text", text: "Audit complete." }],
        details: { progress: 100 },
      });

      const critical = findings.filter(f => f.severity === "critical").length;
      const warning = findings.filter(f => f.severity === "warning").length;
      const info = findings.filter(f => f.severity === "info").length;

      const report = [
        `# UI Consistency Audit Report`,
        ``,
        `**Scope:** ${params.scope || "src"}`,
        `**Files audited:** ${files.length}`,
        ``,
        `## Findings Summary`,
        `- Critical: ${critical}`,
        `- Warning: ${warning}`,
        `- Info: ${info}`,
        ``,
        `## Detailed Findings`,
        ...findings.map(f => `### [${f.severity.toUpperCase()}] ${f.file}\n- ${f.issue}`),
      ].join("\n");

      return {
        content: [{ type: "text", text: report }],
        details: {
          filesAudited: files.length,
          critical,
          warning,
          info,
          findings,
          designSystemLoaded: true,
        },
      };
    },
  });
}

// ─── Tool: ui_consistency_generate_design_system ────────────────────────────

/**
 * Register the `ui_consistency_generate_design_system` tool that creates STYLE_PICK.md,
 * DESIGN_DNA.md, and COMPONENT_PLAN.md from codebase analysis.
 * @param pi - Extension API used to register the tool.
 */
function registerGenerateTool(pi: ExtensionAPI) {
  pi.registerTool({
    name: "ui_consistency_generate_design_system",
    label: "Generate Design System",
    description: "Generate STYLE_PICK.md, DESIGN_DNA.md, and COMPONENT_PLAN.md from codebase analysis",
    promptSnippet: "Generate design system documents from project analysis",
    parameters: Type.Object({
      force: Type.Optional(Type.Boolean({ description: "Overwrite existing design system" })),
    }),
    async execute(toolCallId, params, signal, onUpdate, ctx) {
      if (signal?.aborted) return { content: [{ type: "text", text: "Cancelled" }] };

      const cwd = ctx.cwd;

      if (hasDesignSystem(cwd) && !params.force) {
        return {
          content: [{ type: "text", text: "Design system already exists. Use force=true to overwrite." }],
          details: { error: "already_exists" },
        };
      }

      onUpdate?.({
        content: [{ type: "text", text: "Analyzing codebase for design patterns..." }],
        details: { progress: 10 },
      });

      // Extract colors
      const colorResult = await pi.exec("bash", ["-c", `
        grep -roh '#[0-9a-fA-F]\{3,8\}' src/ --include="*.css" --include="*.tsx" --include="*.jsx" 2>/dev/null | sort | uniq -c | sort -rn | head -10 || echo "No colors found"
      `], { cwd });

      onUpdate?.({
        content: [{ type: "text", text: "Extracting typography..." }],
        details: { progress: 30 },
      });

      // Extract fonts
      const fontResult = await pi.exec("bash", ["-c", `
        grep -roh 'font-family:[^;]*' src/ --include="*.css" 2>/dev/null | sort | uniq -c | sort -rn | head -5 || echo "No fonts found"
      `], { cwd });

      onUpdate?.({
        content: [{ type: "text", text: "Generating design system documents..." }],
        details: { progress: 60 },
      });

      // Create design system directory
      const { mkdirSync, writeFileSync } = await import("node:fs");
      const dsDir = join(cwd, DESIGN_SYSTEM_DIR);
      mkdirSync(dsDir, { recursive: true });

      const colors = colorResult.stdout.trim() || "No colors detected";
      const fonts = fontResult.stdout.trim() || "No fonts detected";

      // Generate STYLE_PICK.md
      const stylePick = `# STYLE_PICK

## Color Palette

Extracted from codebase:
\`\`\`
${colors}
\`\`\`

## Typography

Extracted from codebase:
\`\`\`
${fonts}
\`\`\`

## Spacing

Base unit: 4px
Scale: xs (4px), sm (8px), md (16px), lg (24px), xl (32px), 2xl (48px)

## Border Radius

Scale: sm (4px), md (8px), lg (12px), full (9999px)

## Shadows

Scale: sm (0 1px 2px rgba(0,0,0,0.05)), md (0 4px 6px rgba(0,0,0,0.1)), lg (0 10px 15px rgba(0,0,0,0.1))
`;

      // Generate DESIGN_DNA.md
      const designDna = `# DESIGN_DNA

## Mood
Professional, clean, modern

## Trust Signals
Formal but approachable

## Density
Balanced

## Visual Rhythm
Grid-based layout with consistent spacing

## Anti-patterns
- Avoid hardcoded colors
- Avoid inline styles
- Avoid magic numbers

## Accessibility Baseline
- WCAG 2.1 AA contrast
- Focus indicators on all interactive elements
- Minimum 44px touch targets
`;

      // Generate COMPONENT_PLAN.md
      const componentPlan = `# COMPONENT_PLAN

## Button

### States
- default, hover, active, focus, disabled, loading

### Sizes
- sm, md, lg

### Verification
- [ ] All states render correctly
- [ ] Focus ring visible
- [ ] Loading state accessible

## Input

### States
- default, focus, error, disabled

### Sizes
- sm, md, lg

## Card

### States
- default, hover, active

### Variants
- outlined, filled, elevated
`;

      writeFileSync(join(dsDir, "STYLE_PICK.md"), stylePick);
      writeFileSync(join(dsDir, "DESIGN_DNA.md"), designDna);
      writeFileSync(join(dsDir, "COMPONENT_PLAN.md"), componentPlan);

      onUpdate?.({
        content: [{ type: "text", text: "Design system generated successfully." }],
        details: { progress: 100 },
      });

      return {
        content: [{ type: "text", text: `Design system generated in ${dsDir}/\n\nFiles created:\n- STYLE_PICK.md\n- DESIGN_DNA.md\n- COMPONENT_PLAN.md` }],
        details: {
          filesCreated: ["STYLE_PICK.md", "DESIGN_DNA.md", "COMPONENT_PLAN.md"],
          directory: dsDir,
        },
      };
    },
  });
}

// ─── Tool: ui_consistency_fix ───────────────────────────────────────────────

/**
 * Register the `ui_consistency_fix` tool that applies automatic fixes to UI files.
 * @param pi - Extension API used to register the tool.
 */
function registerFixTool(pi: ExtensionAPI) {
  pi.registerTool({
    name: "ui_consistency_fix",
    label: "UI Consistency Fix",
    description: "Apply fixes to UI files based on audit findings",
    promptSnippet: "Apply UI consistency fixes from audit",
    parameters: Type.Object({
      file: Type.String({ description: "File path to fix" }),
      mode: Type.Optional(StringEnum(["simple", "medium", "hard"] as const)),
    }),
    async execute(toolCallId, params, signal, onUpdate, ctx) {
      if (signal?.aborted) return { content: [{ type: "text", text: "Cancelled" }] };

      const cwd = ctx.cwd;
      const filePath = join(cwd, params.file);

      if (!existsSync(filePath)) {
        return {
          content: [{ type: "text", text: `File not found: ${params.file}` }],
          details: { error: "file_not_found" },
        };
      }

      const mode = params.mode || "medium";

      if (mode === "hard") {
        return {
          content: [{ type: "text", text: "Hard mode: no automatic fixes applied. Review audit report manually." }],
          details: { mode: "hard", fixed: false },
        };
      }

      onUpdate?.({
        content: [{ type: "text", text: `Analyzing ${params.file}...` }],
        details: { progress: 20 },
      });

      const content = readFileSync(filePath, "utf-8");
      let fixed = content;
      let changes = 0;

      // Simple fixes: replace common hardcoded colors with CSS variables
      if (mode === "simple" || mode === "medium") {
        const colorMap: Record<string, string> = {
          "#fff": "var(--color-background)",
          "#ffffff": "var(--color-background)",
          "#000": "var(--color-text)",
          "#000000": "var(--color-text)",
          "#333": "var(--color-text-secondary)",
          "#333333": "var(--color-text-secondary)",
        };

        for (const [hardcoded, token] of Object.entries(colorMap)) {
          const regex = new RegExp(hardcoded.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "gi");
          if (regex.test(fixed)) {
            fixed = fixed.replace(regex, token);
            changes++;
          }
        }
      }

      onUpdate?.({
        content: [{ type: "text", text: changes > 0 ? `Applied ${changes} fixes.` : "No automatic fixes applicable." }],
        details: { progress: 100 },
      });

      if (changes > 0) {
        const { writeFileSync } = await import("node:fs");
        writeFileSync(filePath, fixed);
      }

      return {
        content: [{ type: "text", text: changes > 0 ? `Fixed ${changes} issues in ${params.file}` : `No fixes applied to ${params.file}` }],
        details: {
          file: params.file,
          changes,
          mode,
        },
      };
    },
  });
}

// ─── Command: /ui-consistency ───────────────────────────────────────────────

/**
 * Register the `/ui-consistency` slash command and its subcommands.
 * @param pi - Extension API used to register the command.
 */
function registerCommand(pi: ExtensionAPI) {
  pi.registerCommand("ui-consistency", {
    description: "UI Consistency workflow: /ui-consistency scan|audit|generate|fix [args]",
    handler: async (args, ctx) => {
      const parts = args.trim().split(/\s+/);
      const subcommand = parts[0] || "help";

      switch (subcommand) {
        case "scan": {
          ctx.ui.notify("Running UI consistency scan...", "info");
          // Trigger the tool
          pi.sendUserMessage(`Run ui_consistency_scan with scope="${parts[1] || "src"}"`, { deliverAs: "followUp" });
          break;
        }
        case "audit": {
          ctx.ui.notify("Running UI consistency audit...", "info");
          pi.sendUserMessage(`Run ui_consistency_audit with scope="${parts[1] || "src"}"`, { deliverAs: "followUp" });
          break;
        }
        case "generate": {
          ctx.ui.notify("Generating design system...", "info");
          pi.sendUserMessage("Run ui_consistency_generate_design_system", { deliverAs: "followUp" });
          break;
        }
        case "fix": {
          if (!parts[1]) {
            ctx.ui.notify("Usage: /ui-consistency fix <file>", "warning");
            return;
          }
          ctx.ui.notify(`Fixing ${parts[1]}...`, "info");
          pi.sendUserMessage(`Run ui_consistency_fix with file="${parts[1]}"`, { deliverAs: "followUp" });
          break;
        }
        case "help":
        default: {
          const help = [
            "UI Consistency Commands:",
            "  /ui-consistency scan [path]     — Scan and classify UI files",
            "  /ui-consistency audit [path]    — Audit against design system",
            "  /ui-consistency generate        — Generate design system documents",
            "  /ui-consistency fix <file>      — Apply fixes to a file",
          ].join("\n");
          ctx.ui.notify(help, "info");
        }
      }
    },
  });
}

// ─── Hooks ──────────────────────────────────────────────────────────────────

/**
 * Register event hooks for session start and before-agent-start lifecycle events.
 * @param pi - Extension API used to register the hooks.
 */
function registerHooks(pi: ExtensionAPI) {
  // Session start: check for design system and notify
  pi.on("session_start", async (_event, ctx) => {
    const cwd = ctx.cwd;
    if (!hasDesignSystem(cwd)) {
      ctx.ui.setStatus("ui-consistency", "⚠ No design system");
    } else {
      ctx.ui.setStatus("ui-consistency", "✓ Design system ready");
    }
  });

  // Before agent start: inject design system context for UI tasks
  pi.on("before_agent_start", async (event, ctx) => {
    const cwd = ctx.cwd;
    const prompt = event.prompt.toLowerCase();

    // Check if this is a UI-related task
    const uiKeywords = ["ui", "ux", "component", "style", "css", "design", "button", "input", "card", "layout", "theme", "color", "typography", "spacing"];
    const isUiTask = uiKeywords.some(kw => prompt.includes(kw));

    if (isUiTask && hasDesignSystem(cwd)) {
      const ds = readDesignSystem(cwd);
      if (ds) {
        return {
          message: {
            customType: "ui-consistency-context",
            content: "Design system is available at .gsd/ui-gates/. Reference STYLE_PICK.md for colors, typography, and spacing before making UI changes.",
            display: false,
          },
        };
      }
    }

    return undefined;
  });
}

// ─── Tool: ui_consistency_self_test ─────────────────────────────────────────

/**
 * Register the `ui_consistency_self_test` tool that runs the built-in validation suite.
 * @param pi - Extension API used to register the tool.
 */
function registerSelfTestTool(pi: ExtensionAPI) {
  pi.registerTool({
    name: "ui_consistency_self_test",
    label: "UI Consistency Self Test",
    description: "Run the extension's built-in validation test suite to verify installation integrity",
    promptSnippet: "Verify UI consistency extension installation",
    parameters: Type.Object({}),
    async execute(toolCallId, params, signal, onUpdate, ctx) {
      if (signal?.aborted) return { content: [{ type: "text", text: "Cancelled" }] };

      onUpdate?.({
        content: [{ type: "text", text: "Running self-test suite..." }],
        details: { progress: 10 },
      });

      // Find the test directory relative to this extension
      const { dirname, join } = await import("node:path");
      const { fileURLToPath } = await import("node:url");
      const extensionDir = dirname(fileURLToPath(import.meta.url));
      const testRunner = join(extensionDir, "skills", "ui-consistency", "tests", "run_all_tests.py");

      if (!existsSync(testRunner)) {
        return {
          content: [{ type: "text", text: "Test runner not found. Extension may be incomplete." }],
          details: { error: "test_runner_missing", path: testRunner },
        };
      }

      onUpdate?.({
        content: [{ type: "text", text: "Found test runner, executing..." }],
        details: { progress: 30 },
      });

      const result = await pi.exec("python3", [testRunner], { cwd: dirname(testRunner) });

      onUpdate?.({
        content: [{ type: "text", text: "Tests complete." }],
        details: { progress: 100 },
      });

      const passed = result.stdout.includes("passed") ? parseInt(result.stdout.match(/(\d+) passed/)?.[1] || "0") : 0;
      const failed = result.stdout.includes("failed") ? parseInt(result.stdout.match(/(\d+) failed/)?.[1] || "0") : 0;

      const summary = [
        `# UI Consistency Extension Self-Test`,
        ``,
        result.stdout.includes("0 failed")
          ? `✅ All tests passed (${passed} total)`
          : `⚠️ ${failed} test(s) failed out of ${passed + failed}`,
        ``,
        `## Test Output`,
        "```",
        result.stdout.slice(-800),
        "```",
      ].join("\n");

      return {
        content: [{ type: "text", text: summary }],
        details: {
          passed,
          failed,
          testRunner,
          allPassed: failed === 0,
        },
      };
    },
  });
}

// ─── Default Export ─────────────────────────────────────────────────────────

/**
 * Activate the UI Consistency extension by registering all tools, commands, and hooks.
 * @param pi - Extension API provided by the host runtime.
 */
export default function registerExtension(pi: ExtensionAPI) {
  registerScanTool(pi);
  registerAuditTool(pi);
  registerGenerateTool(pi);
  registerFixTool(pi);
  registerSelfTestTool(pi);
  registerCommand(pi);
  registerHooks(pi);
}
