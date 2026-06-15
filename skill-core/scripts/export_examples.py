#!/usr/bin/env python3
"""Export skill-forge/built/<theme>/<skill> → examples/<theme>/<skill>."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

BUILT = "skill-forge/built"
DEMO_SKILL_NAMES = ("simple-readme-writer", "medium-commit-message", "complex-pr-review")


def iter_built_skills(built_root: Path) -> list[tuple[str, str, Path]]:
    out: list[tuple[str, str, Path]] = []
    if not built_root.is_dir():
        return out
    for theme_dir in sorted(built_root.iterdir()):
        if not theme_dir.is_dir():
            continue
        for skill_dir in sorted(theme_dir.iterdir()):
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").is_file():
                out.append((theme_dir.name, skill_dir.name, skill_dir))
    return out


def _preserve_demo(repo: Path) -> dict[str, Path]:
    """Save legacy demo skills from examples/demo/, flat paths, or github-upload."""
    examples = repo / "examples"
    preserved: dict[str, Path] = {}
    for name in DEMO_SKILL_NAMES:
        for candidate in (
            examples / "demo" / name,
            examples / name,
            repo / "github-upload" / "examples" / name,
        ):
            if candidate.is_dir() and (candidate / "SKILL.md").is_file():
                preserved[name] = candidate
                break
    return preserved


def export_examples(repo: Path, *, clean: bool = True) -> int:
    repo = repo.resolve()
    built_root = repo / BUILT
    examples = repo / "examples"
    preserved = _preserve_demo(repo)

    if clean and examples.exists():
        shutil.rmtree(examples)
    examples.mkdir(parents=True, exist_ok=True)

    n = 0
    try:
        for theme, skill, src in iter_built_skills(built_root):
            dest = examples / theme / skill
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(src, dest)
            n += 1
    except Exception:
        if examples.exists():
            shutil.rmtree(examples, ignore_errors=True)
        raise

    demo_dir = examples / "demo"
    if preserved:
        demo_dir.mkdir(parents=True, exist_ok=True)
        for name, src in preserved.items():
            dest = demo_dir / name
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(src, dest)
            n += 1

    readme = examples / "README.md"
    lines = [
        "# Examples（按 theme 分组）",
        "",
        "与 `skill-forge/built/<theme>/<skill>` 同构。安装示例：",
        "",
        "```bash",
        "python skill-core/skill.py install examples/student-homework/homework-assistant --host cursor --scope project",
        "python skill-core/skill.py install examples/research/research-survey --host cursor --scope global",
        "```",
        "",
        "## Themes",
        "",
    ]
    for theme in sorted({t for t, _, _ in iter_built_skills(built_root)}):
        skills = [s for t, s, _ in iter_built_skills(built_root) if t == theme]
        lines.append(f"### `{theme}/` ({len(skills)} skills)")
        for s in skills:
            lines.append(f"- `{s}`")
        lines.append("")
    if demo_dir.is_dir():
        demos = sorted(d.name for d in demo_dir.iterdir() if d.is_dir())
        lines.append(f"### `demo/` ({len(demos)} 模板 skill)")
        for d in demos:
            lines.append(f"- `{d}`")
        lines.append("")
    lines.append("重新导出：`python skill-core/scripts/export_examples.py`")
    readme.write_text("\n".join(lines), encoding="utf-8")
    return n


def main() -> int:
    repo = Path(__file__).resolve().parents[2]
    count = export_examples(repo, clean=True)
    print(f"exported {count} skill(s) → {repo / 'examples'} (theme-grouped)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
