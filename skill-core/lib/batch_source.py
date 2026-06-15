"""Parse lightweight .skill.md / .skill.txt sources into full IR."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

SECTION_ALIASES = {
    "goal": "1",
    "context": "1",
    "constraints": "1",
    "inputs": "2",
    "outputs": "3",
    "profile": "3",
    "steps": "5",
    "execution": "5",
    "decision": "6",
    "tools": "7",
    "failures": "10",
    "deps": "12",
    "depends": "12",
    "version": "13",
}


@dataclass
class SkillSource:
    path: Path
    name: str
    meta: dict[str, Any] = field(default_factory=dict)
    sections: dict[str, str] = field(default_factory=dict)


def parse_source_file(path: Path) -> SkillSource:
    text = path.read_text(encoding="utf-8")
    suffix = path.suffix.lower()
    if path.name.endswith(".skill.md") or (suffix == ".md" and path.name != "THEME.md"):
        return _parse_markdown_source(path, text)
    return _parse_text_source(path, text)


def source_to_ir(source: SkillSource, theme: str = "") -> str:
    name = source.name
    meta = source.meta
    profile = meta.get("profile", "narrative")
    status = meta.get("status", "experimental")
    version = meta.get("version", "0.1.0")
    host = meta.get("host", "any")

    goal = _section(source, "goal") or f"Provide the {name} workflow."
    context = _section(source, "context") or "Author requests this capability."
    constraints = _section(source, "constraints") or "- 时间：single session\n- 精度：best-effort"
    inputs = _section(source, "inputs") or "- request: string — author request — validation: non-empty"
    outputs = _section(source, "outputs") or f"**Profile:** {profile}"
    steps = _section(source, "steps") or _section(source, "execution") or "1. ASK author for required inputs"
    decision = _section(source, "decision") or "IF input missing → ASK author"
    tools = _section(source, "tools") or "| Portable ID | Use | Constraints |\n| ask_user | clarify | |"
    failures = _section(source, "failures") or _default_failures()
    deps = _section(source, "deps") or _section(source, "depends") or "depends_on: []\nprovides:\n  - " + name

    if not failures.strip().startswith("#"):
        failures = _failures_to_ir(failures)

    if not tools.strip().startswith("|"):
        tools = _tools_to_table(tools)

    if not steps.strip()[0].isdigit():
        steps = _lines_to_numbered(steps)

    theme_line = f"\nTheme: {theme}\n" if theme else ""

    return f"""{name}

---

# 0. Compilation Target

```yaml
host: {host}
invocation: {meta.get('invocation', 'auto')}
output_profile: {profile}
```

---

# 1. Intent（意图）
{theme_line}
## Goal
{goal.strip()}

## Context
{context.strip()}

## Constraints
{constraints.strip() if constraints.strip().startswith('-') else '- ' + constraints.strip()}

---

# 2. Inputs（输入定义）

## Required Inputs
{inputs.strip() if 'Required' not in inputs else inputs}

---

# 3. Outputs（输出定义）

{outputs.strip() if 'Profile' in outputs else f'**Profile:** {profile}'}

---

# 5. Execution Plan（执行流程）

{steps.strip()}

---

# 6. Decision Logic（决策系统）

```
{decision.strip()}
```

---

# 7. Tool / API Binding（工具绑定）

{tools.strip()}

---

# 10. Failure Modes（失败模式）

{failures.strip()}

---

# 12. Skill Graph Dependencies（依赖）

```yaml
{deps.strip() if deps.strip().startswith('depends') else 'depends_on: []\\nprovides:\\n  - ' + name}
```

---

# 13. Versioning（版本系统）

```yaml
version: "{version}"
status: {status}
```
"""


def _parse_markdown_source(path: Path, text: str) -> SkillSource:
    meta: dict[str, Any] = {}
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3 and yaml:
            meta = yaml.safe_load(parts[1]) or {}
            body = parts[2]

    name = str(meta.get("name") or _name_from_path(path))
    sections: dict[str, str] = {}

    for match in re.finditer(r"^#\s+(.+)$([\s\S]*?)(?=^#\s+|\Z)", body, re.MULTILINE):
        title = match.group(1).strip().lower()
        content = match.group(2).strip()
        key = title.split()[0].lower()
        sections[key] = content
        for alias, _ in SECTION_ALIASES.items():
            if alias in title.lower():
                sections[alias] = content

    return SkillSource(path=path, name=name, meta=meta if isinstance(meta, dict) else {}, sections=sections)


def _parse_text_source(path: Path, text: str) -> SkillSource:
    meta: dict[str, Any] = {}
    sections: dict[str, str] = {}
    current: str | None = None
    buf: list[str] = []

    def flush() -> None:
        nonlocal buf, current
        if current and buf:
            sections[current] = "\n".join(buf).strip()
        buf = []

    for line in text.splitlines():
        kv = re.match(r"^([a-z_]+)\s*:\s*(.*)$", line, re.I)
        if kv and kv.group(1).lower() in (
            "name", "profile", "status", "version", "host", "invocation", "goal", "context"
        ):
            flush()
            key = kv.group(1).lower()
            val = kv.group(2).strip()
            if key in ("name", "profile", "status", "version", "host", "invocation"):
                meta[key] = val
            else:
                current = key
                buf = [val] if val else []
            continue

        header = re.match(r"^\[(.+)\]$", line.strip())
        if header:
            flush()
            current = header.group(1).lower()
            continue

        if current:
            buf.append(line)
        elif line.strip().startswith("-"):
            sections.setdefault("steps", "")
            sections["steps"] += line + "\n"

    flush()
    name = str(meta.get("name") or _name_from_path(path))
    return SkillSource(path=path, name=name, meta=meta, sections=sections)


def _name_from_path(path: Path) -> str:
    stem = path.stem
    for suffix in (".skill",):
        if stem.endswith(suffix.replace(".", "")):
            pass
    stem = re.sub(r"\.skill$", "", stem, flags=re.I)
    stem = re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-")
    return stem or "unnamed-skill"


def _section(source: SkillSource, key: str) -> str:
    return source.sections.get(key, "")


def _lines_to_numbered(text: str) -> str:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    out = []
    for i, line in enumerate(lines, 1):
        line = re.sub(r"^[-*]\s*", "", line)
        if re.match(r"^\d+\.", line):
            out.append(line)
        else:
            out.append(f"{i}. {line}")
    return "\n".join(out)


def _tools_to_table(text: str) -> str:
    rows = ["| Portable ID | Use | Constraints |", "|-------------|-----|-------------|"]
    for line in text.splitlines():
        line = line.strip().lstrip("-")
        if not line:
            continue
        if "|" in line:
            tid = line.split("|")[0].strip()
        else:
            tid = line.split()[0].strip()
        rows.append(f"| {tid} | | |")
    return "\n".join(rows)


def _failures_to_ir(text: str) -> str:
    blocks = []
    for i, line in enumerate(text.splitlines(), 1):
        line = line.strip().lstrip("-")
        if not line:
            continue
        if line.startswith("F") and ":" in line:
            fid, rest = line.split(":", 1)
            parts = [p.strip() for p in rest.split("|")]
            name = parts[0] if parts else "error"
            signal = parts[1] if len(parts) > 1 else name
            recovery = parts[2] if len(parts) > 2 else "ask author"
            blocks.append(
                f"## {fid.strip()}: {name}\n- Signal: {signal}\n- Recovery: {recovery}\n- Severity: block"
            )
        else:
            blocks.append(
                f"## F{i}: error-{i}\n- Signal: {line}\n- Recovery: ask author\n- Severity: block"
            )
    return "\n\n".join(blocks[:5]) if blocks else _default_failures()


def _default_failures() -> str:
    return """## F1: missing-input
- Signal: required input empty
- Recovery: ask author
- Severity: block

## F2: out-of-scope
- Signal: request outside skill scope
- Recovery: clarify with author
- Severity: degrade

## F3: tool-failure
- Signal: tool or command fails
- Recovery: report error and stop
- Severity: block"""
