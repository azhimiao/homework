"""Migrate legacy rules and commands to Agent Skills."""

from __future__ import annotations

import re
from pathlib import Path

from .scaffold import scaffold

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def migrate_file(
    source: Path,
    name: str,
    out_root: Path,
    source_type: str = "auto",
) -> Path:
    source = source.resolve()
    if not source.exists():
        raise FileNotFoundError(source)

    kind = source_type if source_type != "auto" else _detect_type(source)
    body, description, manual = _read_source(source, kind)

    if not NAME_RE.match(name):
        raise ValueError(f"Invalid skill name '{name}'")

    dest = out_root / name
    if dest.exists():
        raise FileExistsError(f"{dest} already exists")

    scaffold(name, out_root)

    skill_md = _build_skill_md(name, description, body, manual)
    (dest / "SKILL.md").write_text(skill_md, encoding="utf-8")

    ir_note = f"""# Migrated Skill: {name}

> Auto-generated from `{source.name}` ({kind}). Review and expand IR sections.

---

# 0. Compilation Target

```yaml
host: any
invocation: {"manual" if manual else "auto"}
```

---

# 1. Intent（意图）

## Goal
Migrated from {kind}: {description or name}

## Context
See original source: {source.name}

## Constraints
- 时间：single session
- 精度：best-effort

---

# 5. Execution Plan（执行流程）

1. READ migrated instructions in SKILL.md body
2. FOLLOW original rule/command workflow verbatim

---

# 10. Failure Modes（失败模式）

## F1: ambiguous-request
- Signal: request outside migrated scope
- Recovery: ask author for clarification
- Severity: block

## F2: missing-context
- Signal: required project context unavailable
- Recovery: ask author or read project files
- Severity: degrade

## F3: outdated-rule
- Signal: migrated source changed on disk
- Recovery: re-run skill migrate or update IR manually
- Severity: degrade

---

# 13. Versioning（版本系统）

```yaml
version: "0.1.0"
status: experimental
```
"""
    (dest / "references" / "ir.md").write_text(ir_note, encoding="utf-8")
    return dest


def migrate_scan(project: Path, out_root: Path) -> list[Path]:
    project = project.resolve()
    created: list[Path] = []

    for mdc in project.glob(".cursor/rules/**/*.mdc"):
        if _should_migrate_mdc(mdc):
            name = _slug(mdc.stem)
            if not (out_root / name).exists():
                created.append(migrate_file(mdc, name, out_root, "mdc"))

    commands_dir = project / ".cursor" / "commands"
    if commands_dir.exists():
        for cmd in commands_dir.glob("*.md"):
            name = _slug(cmd.stem)
            if not (out_root / name).exists():
                created.append(migrate_file(cmd, name, out_root, "command"))

    cursorrules = project / ".cursorrules"
    if cursorrules.exists() and not (out_root / "cursorrules").exists():
        created.append(migrate_file(cursorrules, "cursorrules", out_root, "cursorrules"))

    return created


def _detect_type(source: Path) -> str:
    if source.suffix == ".mdc":
        return "mdc"
    if source.parent.name == "commands":
        return "command"
    if source.name == ".cursorrules":
        return "cursorrules"
    return "markdown"


def _read_source(source: Path, kind: str) -> tuple[str, str, bool]:
    text = source.read_text(encoding="utf-8")
    description = ""
    body = text
    manual = kind in ("command",)

    if kind == "mdc":
        fm, body = _split_mdc(text)
        description = str(fm.get("description", ""))
        manual = bool(fm.get("alwaysApply")) is False
    elif kind == "command":
        description = f"Slash command migrated from {source.name}"
        manual = True
    elif kind == "cursorrules":
        description = "Project rules migrated from .cursorrules"
        manual = False

    return body.strip(), description.strip(), manual


def _split_mdc(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    try:
        import yaml

        fm = yaml.safe_load(parts[1]) or {}
    except Exception:
        fm = {}
    return fm if isinstance(fm, dict) else {}, parts[2].strip()


def _should_migrate_mdc(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    fm, _ = _split_mdc(text)
    if fm.get("alwaysApply") is True:
        return False
    if fm.get("globs"):
        return False
    return bool(fm.get("description"))


def _build_skill_md(name: str, description: str, body: str, manual: bool) -> str:
    desc = description or f"Migrated skill {name}."
    lines = [
        "---",
        f"name: {name}",
        "description: >-",
        f"  {desc}",
    ]
    if manual:
        lines.append("disable-model-invocation: true")
    lines.extend(
        [
            "metadata:",
            '  version: "0.1.0"',
            "  status: experimental",
            "  protocol: skill-protocol-v2",
            "  migrated: true",
            "---",
            "",
            body,
            "",
        ]
    )
    return "\n".join(lines)


def _slug(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    slug = re.sub(r"-+", "-", slug)
    return slug[:64] or "migrated-skill"
