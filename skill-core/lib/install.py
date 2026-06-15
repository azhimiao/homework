"""Install skills to Agent Skills host paths."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from .compiler import compile_skill_dir
from .diff import check_drift
from .validate import validate_skill_dir

HOSTS = {
    "cursor": {
        "global": lambda: Path.home() / ".cursor" / "skills",
        "project": lambda project: Path(project) / ".cursor" / "skills",
    },
    "claude": {
        "global": lambda: Path.home() / ".claude" / "skills",
        "project": lambda project: Path(project) / ".claude" / "skills",
    },
    "agents": {
        "global": lambda: Path.home() / ".agents" / "skills",
        "project": lambda project: Path(project) / ".agents" / "skills",
    },
}

SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "node_modules"}
SKIP_FILES = {".DS_Store"}


@dataclass
class InstallResult:
    source: Path
    target: Path
    host: str
    scope: str


def resolve_install_target(host: str, scope: str, project: Path | None = None) -> Path:
    if host not in HOSTS:
        raise ValueError(f"Unknown host '{host}'. Choose: {', '.join(HOSTS)}")
    if scope not in ("global", "project"):
        raise ValueError("scope must be 'global' or 'project'")

    if scope == "global":
        return HOSTS[host]["global"]()
    if project is None:
        project = Path.cwd()
    return HOSTS[host]["project"](project)


def install_skill(
    skill_dir: Path,
    host: str = "agents",
    scope: str = "global",
    project: Path | None = None,
    force: bool = False,
    compile_first: bool = True,
) -> InstallResult:
    skill_dir = skill_dir.resolve()
    name = skill_dir.name

    if not (skill_dir / "SKILL.md").exists():
        raise FileNotFoundError(f"SKILL.md not found in {skill_dir}")

    if compile_first and (skill_dir / "references" / "ir.md").exists():
        drift = check_drift(skill_dir)
        if drift.drifted or not (skill_dir / "SKILL.md").exists():
            compile_skill_dir(skill_dir)

    errors = validate_skill_dir(skill_dir)
    if errors and not force:
        raise ValueError("validation failed: " + "; ".join(errors))

    base = resolve_install_target(host, scope, project)
    target = base / name

    if target.exists():
        if not force:
            raise FileExistsError(f"already installed at {target} — use --force to overwrite")
        shutil.rmtree(target)

    base.mkdir(parents=True, exist_ok=True)
    shutil.copytree(skill_dir, target, ignore=_ignore_patterns)
    return InstallResult(source=skill_dir, target=target, host=host, scope=scope)


def _ignore_patterns(_dir: str, names: list[str]) -> set[str]:
    ignored = set()
    for name in names:
        if name in SKIP_DIRS or name in SKIP_FILES:
            ignored.add(name)
    return ignored
