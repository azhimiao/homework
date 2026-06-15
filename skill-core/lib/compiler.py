"""Compile Skill Protocol IR to runtime SKILL.md."""

from __future__ import annotations

import re
from pathlib import Path

from .ir_parser import IRDocument, parse_ir

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def compile_skill(ir_text: str, skill_name: str = "") -> str:
    doc = parse_ir(ir_text, skill_name)
    name = _resolve_name(doc, skill_name)
    return _render(doc, name)


def compile_skill_dir(skill_dir: Path, ir_path: Path | None = None) -> Path:
    skill_dir = skill_dir.resolve()
    name = skill_dir.name
    ir_file = ir_path or skill_dir / "references" / "ir.md"
    if not ir_file.exists():
        raise FileNotFoundError(f"IR not found: {ir_file}")

    ir_text = ir_file.read_text(encoding="utf-8")
    output = compile_skill(ir_text, name)
    out_file = skill_dir / "SKILL.md"
    out_file.write_text(output, encoding="utf-8")
    return out_file


def _resolve_name(doc: IRDocument, fallback: str) -> str:
    name = fallback or doc.skill_name
    name = name.strip().lower().replace("_", "-")
    name = re.sub(r"[^a-z0-9-]", "-", name)
    name = re.sub(r"-+", "-", name).strip("-")
    if not NAME_RE.match(name):
        raise ValueError(f"Invalid skill name '{name}'")
    return name


def _render(doc: IRDocument, name: str) -> str:
    version_info = doc.version_info()
    target = doc.compile_target()
    version = str(version_info.get("version", "0.1.0"))
    status = str(version_info.get("status", "experimental"))
    disable = target.get("disable-model-invocation", target.get("invocation") == "manual")

    description = _build_description(doc)
    compatibility = _build_compatibility(doc)
    title = name.replace("-", " ").title()
    steps = doc.execution_steps()
    quick = steps[:5] if steps else ["Follow the workflow below"]

    lines: list[str] = [
        "---",
        f"name: {name}",
        "description: >-",
        _indent_yaml(description),
    ]

    if disable:
        lines.append("disable-model-invocation: true")

    lines.extend(
        [
            "metadata:",
            f'  version: "{version}"',
            f"  status: {status}",
            '  protocol: skill-protocol-v2',
        ]
    )

    if compatibility:
        lines.append(f"compatibility: {compatibility}")

    lines.extend(["---", "", f"# {title}", ""])

    lines.append("## Quick Start")
    lines.append("")
    for i, step in enumerate(quick, 1):
        lines.append(f"{i}. {step}")
    lines.append("")

    lines.append("## Workflow")
    lines.append("")
    if steps:
        for i, step in enumerate(steps, 1):
            lines.append(f"### Step {i}")
            lines.append(step)
            lines.append("")

    decision = doc.decision_logic()
    if decision:
        lines.append("### Decision logic")
        lines.append("")
        lines.append("```")
        lines.append(decision)
        lines.append("```")
        lines.append("")

    inputs = doc.required_inputs()
    optional = doc.optional_inputs()
    if inputs or optional:
        lines.append("## Inputs")
        lines.append("")
        if inputs:
            lines.append("**Required**")
            lines.append("")
            for item in inputs:
                lines.append(f"- {item}")
            lines.append("")
        if optional:
            lines.append("**Optional**")
            lines.append("")
            for item in optional:
                lines.append(f"- {item}")
            lines.append("")

    profile = doc.output_profile()
    lines.append("## Outputs")
    lines.append("")
    lines.append(f"Profile: `{profile}`")
    lines.append("")
    if profile == "narrative":
        lines.append("Deliver with headings: `# Summary`, `# Details`, `# Next Steps`.")
    elif profile == "artifact":
        lines.append("Return artifact paths and a one-paragraph summary.")
    elif profile == "structured":
        lines.append("Return JSON with `result`, `steps`, `confidence`, and `errors`.")
    else:
        lines.append("Return artifacts plus a narrative summary.")
    lines.append("")

    tools = doc.tools_table()
    if tools:
        lines.append("## Tools")
        lines.append("")
        lines.append("| ID | Use | Constraints |")
        lines.append("|----|-----|-------------|")
        for row in tools:
            lines.append(f"| {row['id']} | {row['use']} | {row.get('constraints', '')} |")
        lines.append("")

    subs = doc.sub_skills()
    if subs:
        lines.append("## Sub-skills")
        lines.append("")
        for sub in subs:
            lines.append(f"- **{sub['id']} {sub['name']}** — {sub.get('goal', '')}")
        lines.append("")

    failures = doc.failure_modes()
    lines.append("## Failure Modes")
    lines.append("")
    if failures:
        lines.append("| ID | Signal | Recovery |")
        lines.append("|----|--------|----------|")
        for f in failures:
            lines.append(f"| {f['id']} | {f.get('signal', '')} | {f.get('recovery', '')} |")
    else:
        lines.append("| ID | Signal | Recovery |")
        lines.append("|----|--------|----------|")
        lines.append("| F1 | TODO | TODO |")
    lines.append("")

    tests = doc.l1_tests()
    if tests:
        lines.append("## Verification")
        lines.append("")
        lines.append("| Test | Expected |")
        lines.append("|------|----------|")
        for i, test in enumerate(tests, 1):
            if "→" in test:
                parts = test.split("→", 1)
                lines.append(f"| {parts[0].strip()} | {parts[1].strip()} |")
            else:
                lines.append(f"| T{i} | {test} |")
        lines.append("")

    deps = doc.yaml_block(12)
    if deps.get("depends_on"):
        lines.append("## Dependencies")
        lines.append("")
        for dep in deps["depends_on"]:
            lines.append(f"- `{dep}`")
        lines.append("")

    lines.append("## Additional Resources")
    lines.append("")
    lines.append("- [IR source](references/ir.md)")
    lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def _build_description(doc: IRDocument) -> str:
    goal = doc.goal()
    context = doc.context()
    parts = []
    if goal:
        parts.append(_ensure_third_person(goal))
    if context:
        parts.append(f"Use when {context[0].lower() + context[1:]}" if context else context)
    if not parts:
        parts.append(f"Provides the {doc.skill_name or 'skill'} workflow.")
    text = " ".join(parts)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > 1020:
        text = text[:1017] + "..."
    return text


def _ensure_third_person(sentence: str) -> str:
    sentence = sentence.strip()
    if sentence.lower().startswith(("generate ", "create ", "build ", "run ", "format ", "review ", "validate ")):
        return sentence[0].upper() + sentence[1:]
    replacements = (
        (r"^I ", ""),
        (r"^You ", ""),
        (r"^We ", ""),
    )
    for pat, repl in replacements:
        sentence = re.sub(pat, repl, sentence, flags=re.IGNORECASE)
    return sentence[0].upper() + sentence[1:] if sentence else sentence


def _build_compatibility(doc: IRDocument) -> str:
    constraints = doc.constraints()
    if not constraints:
        return ""
    bits = []
    for c in constraints:
        if "工具" in c or "tool" in c.lower():
            bits.append(c.split("：", 1)[-1].split(":", 1)[-1].strip())
        elif "git" in c.lower():
            bits.append("Requires git")
    if bits:
        return "; ".join(dict.fromkeys(bits))
    return ""


def _indent_yaml(text: str) -> str:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        trial = (" ".join(current + [word])).strip()
        if len(trial) > 90 and current:
            lines.append("  " + " ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append("  " + " ".join(current))
    return "\n".join(lines)
