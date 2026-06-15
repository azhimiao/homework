"""Generate Markdown compatibility views for non-.md theme assets."""

from __future__ import annotations

from pathlib import Path

COMPAT_SUFFIX = ".md"
SKIP_MD_SUFFIXES = (".compat.md", ".yaml.md", ".json.md", ".py.md", ".sh.md", ".txt.md")

PURPOSE_HINTS: list[tuple[str, str]] = [
    ("eval-", "Skill 编译测试断言（eval）；CI `batch build --test` 读取 YAML 源文件。"),
    ("assignment-catalog", "作业/任务路由 catalog；router skill 打分与 install 列表。"),
    ("job-catalog", "求职路由 catalog。"),
    ("habit-catalog", "健康习惯路由 catalog。"),
    ("survey-questions", "调查问卷结构与题目。"),
    ("partner-survey", "双人问卷结构。"),
    ("session-schema", "session.yaml 字段说明模板。"),
    ("profile-schema", "profile.json 输出 schema。"),
    (".schema.json", "JSON Schema 定义。"),
    ("mcu-devices", "MCU 器件对照表。"),
    ("board-devices", "开发板器件对照表。"),
    ("memory-schema", "记忆宫殿 taxonomy、路径与检索权重；companion-memory Agent CLI。"),
    ("memory_", "companion-memory 脚本；Agent 通过 memory_cli.py 调用。"),
    ("check_", "环境检测脚本；skill Steps 中 `RUN scripts/…`。"),
]


def compat_md_path(source: Path) -> Path:
    """Return sibling path: `foo.yaml` → `foo.yaml.md`."""
    return source.with_name(source.name + COMPAT_SUFFIX)


def is_compat_md(path: Path) -> bool:
    name = path.name
    if not name.endswith(COMPAT_SUFFIX):
        return False
    stem = name[: -len(COMPAT_SUFFIX)]
    return any(stem.endswith(ext) for ext in (".yaml", ".json", ".py", ".sh", ".txt"))


def _purpose_for(name: str) -> str:
    for key, hint in PURPOSE_HINTS:
        if key in name:
            return hint
    ext = Path(name).suffix.lower()
    if ext == ".yaml":
        return "YAML 配置或结构化数据。"
    if ext == ".json":
        return "JSON 结构化数据。"
    if ext == ".py":
        return "Python 脚本。"
    if ext == ".sh":
        return "Shell 脚本。"
    return "非 Markdown 源文件。"


def _fence_lang(path: Path) -> str:
    ext = path.suffix.lower()
    return {".yaml": "yaml", ".yml": "yaml", ".json": "json", ".py": "python", ".sh": "bash", ".txt": "text"}.get(
        ext, ""
    )


def _usage_section(path: Path, rel: str) -> str:
    if path.suffix.lower() != ".py":
        return ""
    script = path.name
    return f"""
## 运行

```bash
python scripts/{script}
```

Skill Steps 引用路径：`scripts/{script}` 或 `refs/{rel}`（编译后位于 `references/refs/`）。
"""


def render_compat_md(source: Path, *, theme_relative: str) -> str:
    content = source.read_text(encoding="utf-8")
    lang = _fence_lang(source)
    purpose = _purpose_for(source.name)
    usage = _usage_section(source, theme_relative)
    return f"""# MD 兼容视图 — `{source.name}`

> **权威源文件**：同目录 `{source.name}`（本文件由 `skill-core` 自动生成，请勿手改；改源文件后重新 `batch build` 或运行 compat 同步。）

| 项 | 值 |
|----|-----|
| 类型 | `{source.suffix.lstrip('.') or 'unknown'}` |
| 路径 | `{theme_relative}` |
| 用途 | {purpose} |

## 内容

```{lang}
{content.rstrip()}
```
{usage}"""


def sync_compat_md_for_file(source: Path, theme_dir: Path) -> Path | None:
    if source.suffix.lower() == ".md":
        return None
    if is_compat_md(source):
        return None
    rel = source.relative_to(theme_dir).as_posix()
    dest = compat_md_path(source)
    dest.write_text(render_compat_md(source, theme_relative=rel), encoding="utf-8")
    return dest


def sync_compat_md_theme(theme_dir: Path) -> list[Path]:
    written: list[Path] = []
    for path in sorted(theme_dir.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() == ".md" and not is_compat_md(path):
            continue
        if path.name in ("THEME.md", "README.md", "theme.md", "readme.md"):
            continue
        if path.suffix.lower() == ".md":
            continue
        result = sync_compat_md_for_file(path, theme_dir)
        if result:
            written.append(result)
    return written


def sync_compat_md_all(themes_dir: Path) -> dict[str, list[Path]]:
    out: dict[str, list[Path]] = {}
    if not themes_dir.exists():
        return out
    for theme_dir in sorted(themes_dir.iterdir()):
        if not theme_dir.is_dir() or theme_dir.name.startswith("_"):
            continue
        files = sync_compat_md_theme(theme_dir)
        if files:
            out[theme_dir.name] = files
    return out
