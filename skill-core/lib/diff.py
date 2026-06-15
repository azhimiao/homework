"""Detect drift between IR and compiled SKILL.md."""

from __future__ import annotations

import difflib
from dataclasses import dataclass
from pathlib import Path

from .compiler import compile_skill
from .ir_parser import parse_ir


@dataclass
class DriftResult:
    skill_dir: Path
    drifted: bool
    diff: str = ""
    message: str = ""


def check_drift(skill_dir: Path, ir_path: Path | None = None) -> DriftResult:
    skill_dir = skill_dir.resolve()
    ir_file = ir_path or skill_dir / "references" / "ir.md"
    skill_md = skill_dir / "SKILL.md"

    if not ir_file.exists():
        return DriftResult(skill_dir, False, message="no ir.md — skip")
    if not skill_md.exists():
        return DriftResult(
            skill_dir,
            True,
            message="SKILL.md missing — run skill compile",
        )

    ir_text = ir_file.read_text(encoding="utf-8")
    expected = compile_skill(ir_text, skill_dir.name)
    actual = skill_md.read_text(encoding="utf-8")

    if _normalize(expected) == _normalize(actual):
        return DriftResult(skill_dir, False, message="in sync")

    diff = "".join(
        difflib.unified_diff(
            actual.splitlines(keepends=True),
            expected.splitlines(keepends=True),
            fromfile="SKILL.md (current)",
            tofile="SKILL.md (from ir.md)",
        )
    )
    return DriftResult(
        skill_dir,
        True,
        diff=diff,
        message="IR and SKILL.md differ — run skill compile",
    )


def _normalize(text: str) -> str:
    return text.replace("\r\n", "\n").strip() + "\n"
