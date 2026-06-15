#!/usr/bin/env python3
"""Skill-Core CLI — full toolchain for Agent Skills."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SKILL_CORE = Path(__file__).resolve().parent
REPO_ROOT = SKILL_CORE.parent
sys.path.insert(0, str(SKILL_CORE))

from lib.compiler import compile_skill_dir  # noqa: E402
from lib.diff import check_drift  # noqa: E402
from lib.export import SCHEMA_PATH, export_ir_json  # noqa: E402
from lib.install import install_skill  # noqa: E402
from lib.migrate import migrate_file, migrate_scan  # noqa: E402
from lib.registry import build_registry, find_skill, list_skills, load_registry  # noqa: E402
from lib.scaffold import scaffold  # noqa: E402
from lib.test_runner import run_tests  # noqa: E402
from lib.validate import validate_skill_dir  # noqa: E402
from lib.batch import FORGE_ROOT, build_all, build_theme, init_theme, list_themes  # noqa: E402
from lib.compat_md import sync_compat_md_all, sync_compat_md_theme  # noqa: E402


def cmd_init(args: argparse.Namespace) -> int:
    root = Path(args.dir).resolve()
    try:
        dest = scaffold(args.name, root)
    except (ValueError, FileExistsError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"created {dest}")
    print(f"  1. edit {dest / 'references' / 'ir.md'}")
    print(f"  2. run: skill compile {dest.name}")
    return 0


def cmd_compile(args: argparse.Namespace) -> int:
    paths = expand_skill_paths(args.paths)
    if not paths:
        print("error: no skill paths given", file=sys.stderr)
        return 2

    ok = True
    for path in paths:
        try:
            if path.is_file():
                skill_dir = path.parent.parent if path.name == "ir.md" else path.parent
                out = compile_skill_dir(skill_dir, ir_path=path)
            else:
                out = compile_skill_dir(path)
            print(f"compiled {out}")
            if args.json:
                skill_dir = path if path.is_dir() else (path.parent.parent if path.name == "ir.md" else path.parent)
                json_path = export_ir_json(skill_dir)
                print(f"exported {json_path}")
        except Exception as exc:
            ok = False
            print(f"error compiling {path}: {exc}", file=sys.stderr)
    return 0 if ok else 1


def cmd_validate(args: argparse.Namespace) -> int:
    return _run_on_skills(args.paths, _validate_one)


def _validate_one(skill_dir: Path) -> bool:
    errors = validate_skill_dir(skill_dir)
    if errors:
        print(f"FAIL {skill_dir.name}")
        for err in errors:
            print(f"  - {err}")
        return False
    print(f"OK   {skill_dir.name}")
    return True


def cmd_test(args: argparse.Namespace) -> int:
    paths = expand_skill_paths(args.paths)
    if not paths:
        print("error: no skill paths given", file=sys.stderr)
        return 2

    ok = True
    for path in paths:
        skill_dir = path if path.is_dir() else path.parent
        failures, passes = run_tests(skill_dir)
        print(f"--- {skill_dir.name} ---")
        for result in passes:
            print(f"  PASS  {result.case_id}: {result.message}")
        for result in failures:
            ok = False
            print(f"  FAIL  {result.case_id}: {result.message}")
        print(f"  {len(passes)} passed, {len(failures)} failed")
    return 0 if ok else 1


def cmd_diff(args: argparse.Namespace) -> int:
    paths = expand_skill_paths(args.paths)
    if not paths:
        print("error: no skill paths given", file=sys.stderr)
        return 2

    ok = True
    for path in paths:
        skill_dir = path if path.is_dir() else path.parent
        result = check_drift(skill_dir)
        if result.drifted:
            ok = False
            print(f"DRIFT {skill_dir.name}: {result.message}")
            if args.verbose and result.diff:
                print(result.diff)
        else:
            print(f"SYNC  {skill_dir.name}: {result.message}")
    return 0 if ok else 1


def cmd_install(args: argparse.Namespace) -> int:
    source = _resolve_skill_source(args.name)
    if source is None:
        print(f"error: skill not found: {args.name}", file=sys.stderr)
        return 1

    project = Path(args.project).resolve() if args.project else None
    try:
        result = install_skill(
            source,
            host=args.host,
            scope=args.scope,
            project=project,
            force=args.force,
            compile_first=not args.no_compile,
        )
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"installed {result.source.name}")
    print(f"  host:  {result.host}")
    print(f"  scope: {result.scope}")
    print(f"  path:  {result.target}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    reg_path = Path(args.registry).resolve() if args.registry else None
    registry = load_registry(reg_path)
    entries = list_skills(registry, tag=args.tag)
    if not entries:
        print("no skills in registry — run: skill registry build")
        return 0

    for entry in entries:
        tags = ",".join(entry.tags or [])
        print(f"{entry.name:28} {entry.version:8} {entry.status:12} {tags}")
        if args.verbose:
            print(f"  {entry.description[:120]}")
            print(f"  path: {entry.path}")
    return 0


def cmd_registry_build(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    out = Path(args.output).resolve() if args.output else root / "registry.json"
    path = build_registry(root, out)
    count = len(load_registry(path).get("skills", []))
    print(f"registry {path} ({count} skills)")
    return 0


def cmd_migrate(args: argparse.Namespace) -> int:
    source = Path(args.source).resolve()
    out_root = Path(args.out).resolve()
    try:
        dest = migrate_file(source, args.name, out_root, args.type)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"migrated {source} → {dest}")
    print(f"  review {dest / 'SKILL.md'} and {dest / 'references' / 'ir.md'}")
    return 0


def cmd_migrate_scan(args: argparse.Namespace) -> int:
    project = Path(args.project).resolve()
    out_root = Path(args.out).resolve()
    try:
        created = migrate_scan(project, out_root)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if not created:
        print("nothing to migrate")
        return 0
    for dest in created:
        print(f"migrated → {dest}")
    return 0


def cmd_export_schema(args: argparse.Namespace) -> int:
    if not SCHEMA_PATH.exists():
        print(f"error: schema not found at {SCHEMA_PATH}", file=sys.stderr)
        return 1
    print(SCHEMA_PATH.read_text(encoding="utf-8"))
    return 0


def cmd_docs(args: argparse.Namespace) -> int:
    index = REPO_ROOT / "docs" / "index.html"
    if not index.exists():
        print(f"error: docs not found at {index}", file=sys.stderr)
        return 1
    print(index.as_uri())
    return 0


def cmd_batch_new_theme(args: argparse.Namespace) -> int:
    try:
        dest = init_theme(args.name, title=args.title or "", description=args.description or "")
    except FileExistsError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"created theme {dest}")
    print(f"  add .skill.md / .skill.txt files")
    print(f"  run: skill batch build {args.name}")
    return 0


def cmd_batch_list(args: argparse.Namespace) -> int:
    themes = list_themes()
    if not themes:
        print("no themes — run: skill batch new-theme <name>")
        return 0
    for t in themes:
        from lib.batch import find_sources

        count = len(find_sources(t))
        print(f"{t.name:24} {count} source(s)")
    return 0


def cmd_batch_build(args: argparse.Namespace) -> int:
    try:
        results = build_theme(args.theme, do_tests=args.test)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return _print_batch_results(results)


def cmd_batch_build_all(args: argparse.Namespace) -> int:
    results = build_all(do_tests=args.test)
    if not results:
        print("no skills built — add themes under skill-forge/themes/")
        return 0
    return _print_batch_results(results)


def cmd_batch_compat(args: argparse.Namespace) -> int:
    themes_dir = FORGE_ROOT / "themes"
    if args.theme:
        written = sync_compat_md_theme(themes_dir / args.theme)
        print(f"compat {args.theme}: {len(written)} file(s)")
        for p in written:
            print(f"  {p.relative_to(themes_dir)}")
        return 0
    all_written = sync_compat_md_all(themes_dir)
    total = sum(len(v) for v in all_written.values())
    print(f"compat all themes: {total} file(s)")
    for theme, files in sorted(all_written.items()):
        if files:
            print(f"  {theme}: {len(files)}")
    return 0


def _print_batch_results(results) -> int:
    ok = True
    for r in results:
        status = "OK  " if r.ok else "FAIL"
        print(f"{status} {r.theme}/{r.output.name}  ← {r.source.name}")
        if not r.ok:
            ok = False
            print(f"      {r.message}")
    print(f"built {sum(1 for r in results if r.ok)}/{len(results)}")
    return 0 if ok else 1


def _resolve_skill_source(name_or_path: str) -> Path | None:
    p = Path(name_or_path)
    if p.exists():
        return p.resolve() if p.is_dir() else p.parent.resolve()
    found = find_skill(name_or_path, root=REPO_ROOT)
    return found


def _run_on_skills(items: list[str], fn) -> int:
    paths = expand_skill_paths(items)
    if not paths:
        print("error: no skill paths given", file=sys.stderr)
        return 2
    ok = all(fn(path if path.is_dir() else path.parent) for path in paths)
    return 0 if ok else 1


def expand_skill_paths(items: list[str]) -> list[Path]:
    paths: list[Path] = []

    def add_tree(p: Path) -> None:
        if (p / "SKILL.md").exists() or (p / "references" / "ir.md").exists():
            paths.append(p)
            return
        if not p.is_dir():
            return
        for child in sorted(p.iterdir()):
            if child.is_dir():
                add_tree(child)

    for item in items:
        p = Path(item).resolve()
        if p.is_file():
            paths.append(p)
        elif p.is_dir():
            add_tree(p)
    return paths


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="skill",
        description="Skill-Core CLI — build, test, install Agent Skills",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Create a new skill from template")
    p_init.add_argument("name")
    p_init.add_argument("--dir", default=str(REPO_ROOT))
    p_init.set_defaults(func=cmd_init)

    p_compile = sub.add_parser("compile", help="Compile IR to SKILL.md")
    p_compile.add_argument("paths", nargs="+")
    p_compile.add_argument("--json", action="store_true")
    p_compile.set_defaults(func=cmd_compile)

    p_validate = sub.add_parser("validate", help="Validate SKILL.md")
    p_validate.add_argument("paths", nargs="+")
    p_validate.set_defaults(func=cmd_validate)

    p_test = sub.add_parser("test", help="Run L0/L1 tests")
    p_test.add_argument("paths", nargs="+")
    p_test.set_defaults(func=cmd_test)

    p_diff = sub.add_parser("diff", help="Check IR drift")
    p_diff.add_argument("paths", nargs="+")
    p_diff.add_argument("-v", "--verbose", action="store_true")
    p_diff.set_defaults(func=cmd_diff)

    p_install = sub.add_parser("install", help="Install skill to host")
    p_install.add_argument("name", help="Skill name (registry) or path")
    p_install.add_argument("--host", choices=["cursor", "claude", "agents"], default="agents")
    p_install.add_argument("--scope", choices=["global", "project"], default="global")
    p_install.add_argument("--project", help="Project dir for scope=project")
    p_install.add_argument("--force", action="store_true")
    p_install.add_argument("--no-compile", action="store_true")
    p_install.set_defaults(func=cmd_install)

    p_list = sub.add_parser("list", help="List registry skills")
    p_list.add_argument("--tag")
    p_list.add_argument("--registry")
    p_list.add_argument("-v", "--verbose", action="store_true")
    p_list.set_defaults(func=cmd_list)

    p_reg = sub.add_parser("registry", help="Registry operations")
    reg_sub = p_reg.add_subparsers(dest="registry_cmd", required=True)
    p_reg_build = reg_sub.add_parser("build", help="Build registry.json")
    p_reg_build.add_argument("--root", default=str(REPO_ROOT))
    p_reg_build.add_argument("--output")
    p_reg_build.set_defaults(func=cmd_registry_build)

    p_migrate = sub.add_parser("migrate", help="Migrate rule/command to skill")
    p_migrate.add_argument("source")
    p_migrate.add_argument("--name", required=True)
    p_migrate.add_argument("--out", default=str(REPO_ROOT))
    p_migrate.add_argument("--type", default="auto", choices=["auto", "mdc", "command", "cursorrules", "markdown"])
    p_migrate.set_defaults(func=cmd_migrate)

    p_mscan = sub.add_parser("migrate-scan", help="Scan project and migrate eligible rules")
    p_mscan.add_argument("--project", default=".")
    p_mscan.add_argument("--out", default=str(REPO_ROOT))
    p_mscan.set_defaults(func=cmd_migrate_scan)

    p_schema = sub.add_parser("schema", help="Print IR JSON Schema")
    p_schema.set_defaults(func=cmd_export_schema)

    p_docs = sub.add_parser("docs", help="Print documentation site URI")
    p_docs.set_defaults(func=cmd_docs)

    p_batch = sub.add_parser("batch", help="Batch skill forge (md/txt sources)")
    batch_sub = p_batch.add_subparsers(dest="batch_cmd", required=True)

    p_bt_new = batch_sub.add_parser("new-theme", help="Create theme folder")
    p_bt_new.add_argument("name", help="Theme slug e.g. dev-tools")
    p_bt_new.add_argument("--title", default="", help="Human title")
    p_bt_new.add_argument("--description", default="", help="Theme description")
    p_bt_new.set_defaults(func=cmd_batch_new_theme)

    p_bt_list = batch_sub.add_parser("list", help="List themes and source counts")
    p_bt_list.set_defaults(func=cmd_batch_list)

    p_bt_build = batch_sub.add_parser("build", help="Build one theme")
    p_bt_build.add_argument("theme")
    p_bt_build.add_argument("--test", action="store_true", help="Run L0/L1 after build")
    p_bt_build.set_defaults(func=cmd_batch_build)

    p_bt_all = batch_sub.add_parser("build-all", help="Build all themes")
    p_bt_all.add_argument("--test", action="store_true")
    p_bt_all.set_defaults(func=cmd_batch_build_all)

    p_bt_compat = batch_sub.add_parser("compat", help="Sync *.yaml.md / *.py.md mirrors only")
    p_bt_compat.add_argument("theme", nargs="?", default="", help="Theme slug (omit for all)")
    p_bt_compat.set_defaults(func=cmd_batch_compat)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
