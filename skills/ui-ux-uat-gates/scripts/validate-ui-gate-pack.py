#!/usr/bin/env python3
"""Read-only validator for GSD UI/UX UAT gate artifacts.

Validates a directory containing STYLE_PICK.md, DESIGN_DNA.md,
COMPONENT_PLAN.md, and UI_VERIFY.md. The script never writes files,
never calls network services, and never mutates GSD state.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

REQUIRED_FILES = ["STYLE_PICK.md", "DESIGN_DNA.md", "COMPONENT_PLAN.md", "UI_VERIFY.md"]
VALID_VERDICTS = {"PASS", "FAIL", "NEEDS_ATTENTION"}
PLACEHOLDER_RE = re.compile(r"(<[^>]+>|\{\{.*?\}\}|\bTBD\b|\bTODO\b|\bFIXME\b|\[INSERT[:\]]|^\s*-\s*$)", re.I | re.M)
BAD_SOURCE_RE = re.compile(r"\b(Lorem ipsum|Acme\b|John Doe|Jane Doe|rest of code|transition:\s*all|linear-gradient\([^)]*(6366f1|8b5cf6|7c3aed|4f46e5|3b82f6))", re.I)
COMMERCIAL_STOCK_RE = re.compile(r"(gettyimages\.com|shutterstock\.com|istockphoto\.com|alamy\.com|stock\.adobe\.com|adobestock\.com)", re.I)
MOTION_CONFLICT_RE = re.compile(r"(gsap|three|@react-three|threejs).*(framer-motion)|framer-motion.*(gsap|three|@react-three|threejs)", re.I | re.S)

@dataclass
class Finding:
    severity: str
    file: str
    rule: str
    message: str


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def has_line_value(text: str, label: str) -> bool:
    m = re.search(rf"^-\s*{re.escape(label)}\s*:\s*(.+)$", text, re.I | re.M)
    return bool(m and m.group(1).strip() and m.group(1).strip() not in {"|", "-"})


def extract_overall_verdict(text: str) -> str | None:
    m = re.search(r"Overall verdict\s*:\s*(PASS|FAIL|NEEDS_ATTENTION)", text, re.I)
    return m.group(1).upper() if m else None


def validate_dir(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    texts: dict[str, str] = {}

    if not root.exists() or not root.is_dir():
        return [Finding("blocker", str(root), "artifact-dir-missing", "Artifact directory does not exist or is not a directory.")]

    for name in REQUIRED_FILES:
        p = root / name
        if not p.exists():
            findings.append(Finding("blocker", name, "missing-artifact", f"Required artifact {name} is missing."))
        else:
            texts[name] = read(p)

    for name, text in texts.items():
        if len(text.strip()) < 80:
            findings.append(Finding("blocker", name, "artifact-too-small", "Artifact is too small to contain useful gate evidence."))
        if PLACEHOLDER_RE.search(text):
            findings.append(Finding("blocker", name, "unresolved-placeholder", "Artifact contains unresolved placeholder/TODO/empty bullet."))

    sp = texts.get("STYLE_PICK.md", "")
    if sp:
        for label in ["Surface", "Style pack", "Selection mode", "Confidence"]:
            if not has_line_value(sp, label):
                findings.append(Finding("blocker", "STYLE_PICK.md", "missing-style-field", f"Missing or empty field: {label}."))
        not_rules = re.search(r"## Not-rules(?P<body>.*?)(\n## |\Z)", sp, re.S)
        if not not_rules or len([l for l in not_rules.group("body").splitlines() if l.strip().startswith("-") and len(l.strip()) > 3]) < 3:
            findings.append(Finding("blocker", "STYLE_PICK.md", "not-rules-insufficient", "STYLE_PICK needs at least three concrete not-rules."))

    dna = texts.get("DESIGN_DNA.md", "")
    if dna:
        for label in ["Label", "Vibe", "Layout / composition", "Motion strategy", "Signature move", "Visual signature"]:
            if not has_line_value(dna, label):
                findings.append(Finding("blocker", "DESIGN_DNA.md", "missing-dna-field", f"Missing or empty field: {label}."))

    cp = texts.get("COMPONENT_PLAN.md", "")
    if cp:
        for label in ["Surface", "STYLE_PICK reference", "DESIGN_DNA reference", "Runtime", "Verdict"]:
            if not has_line_value(cp, label):
                findings.append(Finding("blocker", "COMPONENT_PLAN.md", "missing-component-field", f"Missing or empty field: {label}."))
        if re.search(r"Runtime:\s*(gsap|gsap\+lenis)", cp, re.I) and not re.search(r"Reduced-motion path:\s*(?!\s*$).+", cp, re.I):
            findings.append(Finding("blocker", "COMPONENT_PLAN.md", "missing-reduced-motion", "GSAP/Lenis motion requires a reduced-motion path."))

    uv = texts.get("UI_VERIFY.md", "")
    if uv:
        verdict = extract_overall_verdict(uv)
        if verdict not in VALID_VERDICTS:
            findings.append(Finding("blocker", "UI_VERIFY.md", "missing-overall-verdict", "Overall verdict must be PASS, FAIL, or NEEDS_ATTENTION."))
        for required in ["desktop", "tablet", "mobile", "Console errors", "Failed network requests", "Horizontal scroll", "Focus visible", "Primary flow usable", "Accessibility smoke"]:
            if required.lower() not in uv.lower():
                findings.append(Finding("blocker", "UI_VERIFY.md", "missing-browser-check", f"Missing browser evidence row: {required}."))
        if verdict == "PASS":
            if re.search(r"\|\s*(FAIL|NEEDS_ATTENTION)\s*\|", uv):
                findings.append(Finding("blocker", "UI_VERIFY.md", "pass-with-nonpass-check", "Overall PASS conflicts with FAIL/NEEDS_ATTENTION check rows."))
            blockers = re.search(r"## Blockers(?P<body>.*?)(\n## |\Z)", uv, re.S | re.I)
            if blockers and not re.search(r"None\.?", blockers.group("body"), re.I):
                findings.append(Finding("blocker", "UI_VERIFY.md", "pass-with-blockers", "Overall PASS conflicts with non-empty blockers section."))

    combined = "\n".join(texts.values())
    if BAD_SOURCE_RE.search(combined):
        findings.append(Finding("blocker", "<gate-pack>", "anti-slop-blocker", "Detected placeholder copy, rest-of-code, transition: all, or canonical AI gradient."))
    if COMMERCIAL_STOCK_RE.search(combined):
        findings.append(Finding("blocker", "<gate-pack>", "commercial-stock-url", "Detected commercial-stock image host without license evidence."))
    if MOTION_CONFLICT_RE.search(combined):
        findings.append(Finding("blocker", "<gate-pack>", "motion-stack-conflict", "Detected GSAP/ThreeJS mixed with Framer Motion in one plan/evidence pack."))

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate GSD UI/UX UAT gate artifacts.")
    parser.add_argument("artifact_dir", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    findings = validate_dir(args.artifact_dir)
    blockers = [f for f in findings if f.severity == "blocker"]
    report = {
        "ok": not blockers,
        "artifact_dir": str(args.artifact_dir),
        "blocker_count": len(blockers),
        "findings": [asdict(f) for f in findings],
    }

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        if report["ok"]:
            print("PASS: UI/UX UAT gate pack is complete enough for a completion claim.")
        else:
            print(f"FAIL: {len(blockers)} blocker(s) in UI/UX UAT gate pack.")
            for f in findings:
                print(f"  - [{f.severity}] {f.file}: {f.rule}: {f.message}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
