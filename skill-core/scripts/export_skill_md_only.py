#!/usr/bin/env python3
"""Export markdown-only `skill/` tree (clean layout)."""

from __future__ import annotations

import shutil
from pathlib import Path


def _iter_example_skill_dirs(base: Path):
    if not base.is_dir():
        return
    for child in sorted(base.iterdir()):
        if not child.is_dir() or child.name == "README.md":
            continue
        if (child / "SKILL.md").is_file():
            yield child
        else:
            for sub in sorted(child.iterdir()):
                if sub.is_dir() and (sub / "SKILL.md").is_file():
                    yield sub


def _count_example_skills(examples_dir: Path) -> int:
    return sum(1 for _ in _iter_example_skill_dirs(examples_dir))


def copy_md_tree(src_dir: Path, dst_dir: Path, *, skip_top_dirs: set[str] | None = None) -> int:
    skip = skip_top_dirs or set()
    n = 0
    for md in src_dir.rglob("*.md"):
        rel = md.relative_to(src_dir)
        if rel.parts and rel.parts[0] in skip:
            continue
        out = dst_dir / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(md, out)
        n += 1
    return n


def export_md_only(repo: Path, dst: Path, readme_src: Path | None = None) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir()

    copied = 0
    readme_src = readme_src or repo / "github-upload"
    for name in ("README.md", "UPLOAD.md"):
        p = readme_src / name
        if p.is_file():
            shutil.copy2(p, dst / name)
            copied += 1

    roadmap = repo / "skill-forge" / "themes" / "ROADMAP.md"
    if roadmap.is_file():
        shutil.copy2(roadmap, dst / "ROADMAP.md")
        copied += 1

    docs = readme_src / "docs"
    if docs.is_dir():
        copied += copy_md_tree(docs, dst / "docs")

    examples_src = repo / "examples"
    if examples_src.is_dir():
        for skill_dir in _iter_example_skill_dirs(examples_src):
            rel = skill_dir.relative_to(examples_src)
            copied += copy_md_tree(skill_dir, dst / "examples" / rel)

    themes_src = repo / "skill-forge" / "themes"
    if themes_src.is_dir():
        for theme_dir in sorted(themes_src.iterdir()):
            if not theme_dir.is_dir() or theme_dir.name.startswith("_"):
                continue
            copied += copy_md_tree(theme_dir, dst / "skill-forge" / "themes" / theme_dir.name)

    sf_readme = repo / "skill-forge" / "README.md"
    if sf_readme.is_file():
        out = dst / "skill-forge" / "README.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(sf_readme, out)
        copied += 1

    skill_count = _count_example_skills(examples_src) if examples_src.is_dir() else 0
    themes_list = (
        sorted(d.name for d in (dst / "skill-forge" / "themes").iterdir() if d.is_dir())
        if (dst / "skill-forge" / "themes").is_dir()
        else []
    )

    index = f"""# skill — Markdown-only 包

从 SkillForSkill 仓库导出，**仅含 `.md` 文件**（与 `github-upload` 内容对应，便于阅读与分享）。

## 结构

| 路径 | 内容 |
|------|------|
| **`SKILL.md`** | 本包入口（Agent Skills 根目录） |
| `examples/<theme>/<skill>/SKILL.md` | 各 skill 编译产物（{skill_count} 个，按 theme 分组） |
| `examples/<theme>/<skill>/references/` | 参考文档与 `*.yaml.md` 兼容视图 |
| `skill-forge/themes/<theme>/` | 主题源（`.skill.md`、`THEME.md`、`refs/`） |
| `README.md` | 仓库说明（与 github-upload 相同） |
| `ROADMAP.md` | 十条路线图 |

## 不含

- `skill-core/` 工具链、`.yaml`/`.json`/`.py` 源文件、`registry.json`、CI

## 安装（需完整仓库）

```bash
python skill-core/skill.py install examples/student-homework/homework-assistant --host cursor --scope global
```

## Skills（{skill_count}，见 examples/ 各 theme 子目录）

## Themes（{len(themes_list)}）

{chr(10).join(f'- `{t}`' for t in themes_list)}

## 重新导出

```bash
python skill-core/scripts/export_examples.py
python skill-core/scripts/export_skill_md_only.py
```
"""
    (dst / "INDEX.md").write_text(index, encoding="utf-8")
    copied += 1

    bundle_skill = Path(__file__).resolve().parent.parent / "templates" / "skill-bundle-SKILL.md"
    if bundle_skill.is_file():
        text = bundle_skill.read_text(encoding="utf-8")
        text = text.replace(
            "位于 **`examples/<skill-name>/SKILL.md`**。",
            f"位于 **`examples/<theme>/<skill-name>/SKILL.md`**（共 {skill_count} 个）。",
        )
        (dst / "SKILL.md").write_text(text, encoding="utf-8")
        copied += 1

    bad = [p for p in dst.rglob("*") if p.is_file() and p.suffix.lower() != ".md"]
    missing_theme_readme = []
    ex = dst / "examples"
    if ex.is_dir():
        for d in sorted(ex.iterdir()):
            if d.is_dir() and not (d / "SKILL.md").is_file() and d.name != "README.md":
                if not any((d / c / "SKILL.md").is_file() for c in d.iterdir() if c.is_dir()):
                    missing_theme_readme.append(d.name)

    print(f"copied {copied} top-level items; total md: {len(list(dst.rglob('*.md')))}")
    print(f"examples skills: {skill_count}; themes: {len(themes_list)}")
    print(f"root SKILL.md: {(dst / 'SKILL.md').is_file()}")
    print(f"empty example theme dirs: {missing_theme_readme or 'none'}")
    print(f"non-md files: {len(bad)}")
    print(f"dest: {dst}")


def main() -> int:
    repo = Path(__file__).resolve().parents[2]
    dst = repo / "skill"
    export_md_only(repo, dst)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
