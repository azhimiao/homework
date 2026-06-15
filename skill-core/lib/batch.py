"""Batch build skills from skill-forge themes."""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from .batch_source import parse_source_file, source_to_ir
from .compat_md import sync_compat_md_theme
from .compiler import compile_skill_dir
from .test_runner import run_tests
from .validate import validate_skill_dir

FORGE_ROOT = Path(__file__).resolve().parent.parent.parent / "skill-forge"
THEMES_DIR = FORGE_ROOT / "themes"
BUILT_DIR = FORGE_ROOT / "built"

SOURCE_GLOBS = ("*.skill.md", "*.skill.txt")
SKIP_NAMES = {"THEME.md", "README.md", "theme.md", "readme.md"}


@dataclass
class BuildResult:
    theme: str
    source: Path
    output: Path
    ok: bool
    message: str = ""


def init_theme(name: str, title: str = "", description: str = "") -> Path:
    slug = _slug(name)
    dest = THEMES_DIR / slug
    if dest.exists():
        raise FileExistsError(f"theme exists: {dest}")

    dest.mkdir(parents=True)
    title = title or name.replace("-", " ").title()
    desc = description or f"Skills for {title}."

    theme_md = f"""---
title: {title}
tags: []
status: draft
---

# Theme: {title}

{desc}

## 说明

在本文件夹放入 skill 源文件（`.skill.md` 或 `.skill.txt`），然后运行：

```bash
python skill-core/skill.py batch build {slug}
```

## Skill 源文件格式

见 skill-forge/README.md
"""
    (dest / "THEME.md").write_text(theme_md, encoding="utf-8")

    example = f"""---
name: example-{slug}
profile: narrative
status: experimental
---

# Goal
One sentence: what this skill does.

# Context
When the author should use this skill.

# Steps
1. ASK author for required input
2. GENERATE output in markdown
3. VALIDATE output is non-empty

# Decision
IF input missing → ASK author

# Tools
- ask_user

# Failures
F1: missing-input | empty request | ask author
F2: vague-scope | unclear goal | ask to clarify
F3: empty-output | no content generated | regenerate
"""
    (dest / f"example-{slug}.skill.md").write_text(example, encoding="utf-8")
    return dest


def list_themes() -> list[Path]:
    if not THEMES_DIR.exists():
        return []
    return sorted(p for p in THEMES_DIR.iterdir() if p.is_dir() and not p.name.startswith("_"))


def find_sources(theme_dir: Path) -> list[Path]:
    seen: set[Path] = set()
    sources: list[Path] = []

    def add(path: Path) -> None:
        resolved = path.resolve()
        if resolved in seen:
            return
        if path.name in SKIP_NAMES or path.name.startswith("_"):
            return
        seen.add(resolved)
        sources.append(path)

    for pattern in ("*.skill.md", "*.skill.txt"):
        for path in sorted(theme_dir.glob(pattern)):
            add(path)

    for pattern in ("*.md", "*.txt"):
        for path in sorted(theme_dir.glob(pattern)):
            if path.name.endswith(".skill.md") or path.name.endswith(".skill.txt"):
                continue
            add(path)

    return sources


def build_theme(theme: str, out_root: Path | None = None, do_tests: bool = False) -> list[BuildResult]:
    theme_dir = THEMES_DIR / _slug(theme)
    if not theme_dir.exists():
        raise FileNotFoundError(f"theme not found: {theme_dir}")

    out_base = (out_root or BUILT_DIR) / theme_dir.name
    out_base.mkdir(parents=True, exist_ok=True)

    sync_compat_md_theme(theme_dir)

    results: list[BuildResult] = []
    for source in find_sources(theme_dir):
        try:
            result = _build_one(source, theme_dir, out_base, do_tests)
            results.append(result)
        except Exception as exc:
            results.append(
                BuildResult(theme_dir.name, source, out_base, False, str(exc))
            )
    return results


def build_all(out_root: Path | None = None, do_tests: bool = False) -> list[BuildResult]:
    all_results: list[BuildResult] = []
    for theme_dir in list_themes():
        all_results.extend(build_theme(theme_dir.name, out_root, do_tests))
    return all_results


def _build_one(source: Path, theme_dir: Path, out_base: Path, do_tests: bool) -> BuildResult:
    parsed = parse_source_file(source)
    name = _slug(parsed.name)
    theme = theme_dir.name
    skill_dir = out_base / name

    if skill_dir.exists():
        shutil.rmtree(skill_dir)

    skill_dir.mkdir(parents=True)
    (skill_dir / "references").mkdir()
    (skill_dir / "scripts").mkdir(exist_ok=True)
    (skill_dir / "assets").mkdir(exist_ok=True)

    ir_text = source_to_ir(parsed, theme=theme)
    (skill_dir / "references" / "ir.md").write_text(ir_text, encoding="utf-8")

    # Keep original source for traceability
    shutil.copy2(source, skill_dir / "references" / f"source{source.suffix}")

    eval_yaml = """tests:
  - id: T1
    description: core sections present
    assert:
      sections: ["Quick Start", "Failure Modes"]
      not_contains: ["PLACEHOLDER", "TODO"]
"""
    eval_named = theme_dir / "refs" / f"eval-{name}.yaml"
    eval_src = theme_dir / "refs" / "eval.yaml"
    if eval_named.exists():
        shutil.copy2(eval_named, skill_dir / "references" / "eval.yaml")
    elif eval_src.exists():
        shutil.copy2(eval_src, skill_dir / "references" / "eval.yaml")
    else:
        (skill_dir / "references" / "eval.yaml").write_text(eval_yaml, encoding="utf-8")

    refs = theme_dir / "refs"
    if refs.exists():
        dest_refs = skill_dir / "references" / "refs"
        if dest_refs.exists():
            shutil.rmtree(dest_refs)
        shutil.copytree(refs, dest_refs)

    theme_scripts = theme_dir / "scripts"
    if theme_scripts.exists():
        for script in theme_scripts.iterdir():
            if script.is_file():
                shutil.copy2(script, skill_dir / "scripts" / script.name)

    compile_skill_dir(skill_dir)

    errors = validate_skill_dir(skill_dir)
    if errors:
        return BuildResult(theme, source, skill_dir, False, "; ".join(errors))

    if do_tests:
        failures, _ = run_tests(skill_dir)
        if failures:
            return BuildResult(
                theme,
                source,
                skill_dir,
                False,
                "; ".join(f"{f.case_id}: {f.message}" for f in failures),
            )

    return BuildResult(theme, source, skill_dir, True, "built")


def _slug(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    slug = re.sub(r"-+", "-", slug)
    return slug or "theme"
