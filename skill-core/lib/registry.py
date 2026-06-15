"""Local skill registry for discovery and install-by-name."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

REGISTRY_VERSION = "1.0.0"
DEFAULT_REGISTRY = Path(__file__).resolve().parent.parent.parent / "registry.json"


@dataclass
class RegistryEntry:
    name: str
    version: str
    description: str
    path: str
    status: str = "experimental"
    tags: list[str] | None = None


def _iter_example_skill_dirs(base: Path):
    """Yield skill dirs: examples/<skill> or examples/<theme>/<skill>."""
    if not base.is_dir():
        return
    for child in sorted(base.iterdir()):
        if not child.is_dir() or child.name.startswith("."):
            continue
        if (child / "SKILL.md").is_file():
            yield child
        else:
            for sub in sorted(child.iterdir()):
                if sub.is_dir() and (sub / "SKILL.md").is_file():
                    yield sub


def build_registry(root: Path, out: Path | None = None) -> Path:
    root = root.resolve()
    out = out or root / "registry.json"
    skills: list[dict] = []

    scan_dirs = [root / "skill-core", root / "examples"]
    for base in scan_dirs:
        if not base.exists():
            continue
        if base.name == "skill-core" and (base / "SKILL.md").exists():
            entry = _entry_from_skill(base, root)
            if entry:
                skills.append(entry)
            continue
        if base.name == "examples":
            for child in _iter_example_skill_dirs(base):
                entry = _entry_from_skill(child, root)
                if entry:
                    skills.append(entry)
            continue
        if base.is_dir():
            for child in sorted(base.iterdir()):
                if child.is_dir() and (child / "SKILL.md").exists():
                    entry = _entry_from_skill(child, root)
                    if entry:
                        skills.append(entry)

    payload = {
        "version": REGISTRY_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "skills": skills,
    }
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return out


def load_registry(path: Path | None = None) -> dict:
    reg_path = path or DEFAULT_REGISTRY
    if not reg_path.exists():
        return {"version": REGISTRY_VERSION, "skills": []}
    return json.loads(reg_path.read_text(encoding="utf-8"))


def list_skills(registry: dict | None = None, tag: str | None = None) -> list[RegistryEntry]:
    data = registry or load_registry()
    entries = []
    for item in data.get("skills", []):
        entry = RegistryEntry(
            name=item["name"],
            version=item.get("version", "0.0.0"),
            description=item.get("description", ""),
            path=item["path"],
            status=item.get("status", "experimental"),
            tags=item.get("tags", []),
        )
        if tag and tag not in (entry.tags or []):
            continue
        entries.append(entry)
    return entries


def find_skill(name: str, registry: dict | None = None, root: Path | None = None) -> Path | None:
    data = registry or load_registry()
    for item in data.get("skills", []):
        if item["name"] == name:
            base = root or DEFAULT_REGISTRY.parent
            return (base / item["path"]).resolve()
    return None


def _entry_from_skill(skill_dir: Path, root: Path) -> dict | None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return None

    text = skill_md.read_text(encoding="utf-8")
    fm = _parse_frontmatter(text)
    name = fm.get("name") or skill_dir.name
    desc = str(fm.get("description", "")).replace("\n", " ").strip()
    meta = fm.get("metadata") or {}
    version = meta.get("version", "0.1.0") if isinstance(meta, dict) else "0.1.0"
    status = meta.get("status", "experimental") if isinstance(meta, dict) else "experimental"

    rel = skill_dir.relative_to(root).as_posix()
    tags = _infer_tags(skill_dir, name)

    return {
        "name": name,
        "version": version,
        "description": desc[:200],
        "path": rel,
        "status": status,
        "tags": tags,
    }


def _infer_tags(skill_dir: Path, name: str) -> list[str]:
    tags: list[str] = []
    if name == "skill-core":
        tags.append("meta")
    if (skill_dir / "scripts").exists() and any((skill_dir / "scripts").iterdir()):
        tags.append("scripts")
    parts = skill_dir.parts
    if "examples" in parts:
        tags.append("example")
        idx = parts.index("examples")
        if idx + 2 < len(parts):
            tags.append(f"theme:{parts[idx + 1]}")
    if "commit" in name or "git" in name:
        tags.append("git")
    if "review" in name or "pr" in name:
        tags.append("review")
    return tags


def _parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    if yaml is None:
        return {}
    data = yaml.safe_load(parts[1]) or {}
    return data if isinstance(data, dict) else {}
