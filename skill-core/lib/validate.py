"""Validate runtime SKILL.md against Skill Protocol basics."""

from __future__ import annotations

import re
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
BANNED_VERBS = re.compile(
    r"^\s*(?:[-*]|\d+\.)?\s*(?:understand|analyze|think about|consider)\b",
    re.IGNORECASE,
)


def validate_skill_dir(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [f"Missing SKILL.md in {skill_dir}"]

    text = skill_md.read_text(encoding="utf-8")
    frontmatter, body = _parse_frontmatter(text)

    if frontmatter is None:
        errors.append("SKILL.md must start with YAML frontmatter (---)")
        return errors

    name = frontmatter.get("name")
    if not name:
        errors.append("Frontmatter missing required field: name")
    elif name != skill_dir.name:
        errors.append(f"name '{name}' must match folder '{skill_dir.name}'")
    elif not NAME_RE.match(name):
        errors.append(f"name '{name}' invalid (lowercase, hyphens, no leading/trailing hyphen)")

    desc = frontmatter.get("description")
    if not desc or not str(desc).strip():
        errors.append("Frontmatter missing required field: description")
    elif len(str(desc)) > 1024:
        errors.append(f"description too long ({len(str(desc))} > 1024 chars)")

    if len(text.splitlines()) > 500:
        errors.append(f"SKILL.md too long ({len(text.splitlines())} lines > 500 recommended)")

    body_lower = body.lower()
    if "## quick start" not in body_lower and "## workflow" not in body_lower and "## instructions" not in body_lower:
        errors.append("Body should include ## Quick Start or ## Workflow or ## Instructions")

    failure_hits = len(re.findall(r"\bF[0-9]+\b", body, re.IGNORECASE))
    if failure_hits < 3 and "failure" not in body_lower:
        errors.append("Document at least 3 failure modes (F1/F2/F3 or ## Failure Modes section)")

    for i, line in enumerate(body.splitlines(), 1):
        if BANNED_VERBS.search(line):
            errors.append(f"Line ~{i}: cognitive verb without action — '{line.strip()[:60]}'")
        for match in re.finditer(r"`([^`]+)`", line):
            if "\\" in match.group(1):
                errors.append(f"Line ~{i}: use forward slashes in paths — `{match.group(1)[:50]}`")
                break

    metadata = frontmatter.get("metadata") or {}
    if isinstance(metadata, dict):
        if not metadata.get("version"):
            errors.append("metadata.version recommended (semver)")
        proto = metadata.get("protocol")
        if proto and proto not in ("skill-protocol-v2", "skill-core-v2"):
            errors.append(f"metadata.protocol should be 'skill-protocol-v2' (got '{proto}')")
    else:
        errors.append("metadata should be a mapping")

    ir_file = skill_dir / "references" / "ir.md"
    if ir_file.exists() and "TODO" in skill_md.read_text(encoding="utf-8"):
        errors.append("SKILL.md still contains TODO — run `skill compile`")

    return errors


def _parse_frontmatter(text: str) -> tuple[dict | None, str]:
    if not text.startswith("---"):
        return None, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, text
    if yaml is None:
        return {"_raw": parts[1]}, parts[2]
    data = yaml.safe_load(parts[1]) or {}
    return data, parts[2]
