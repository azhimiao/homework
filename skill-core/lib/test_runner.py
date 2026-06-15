"""Run L0/L1 automated tests for a skill."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

from .compiler import compile_skill
from .diff import check_drift
from .ir_parser import parse_ir
from .validate import validate_skill_dir


@dataclass
class TestCase:
    id: str
    description: str = ""
    assert_contains: list[str] = field(default_factory=list)
    assert_sections: list[str] = field(default_factory=list)
    assert_not_contains: list[str] = field(default_factory=list)


@dataclass
class TestResult:
    case_id: str
    passed: bool
    message: str = ""


def run_tests(skill_dir: Path) -> tuple[list[TestResult], list[TestResult]]:
    """Return (failures, passes) for all tests including built-in L0."""
    skill_dir = skill_dir.resolve()
    results: list[TestResult] = []

    results.extend(_run_l0(skill_dir))
    results.extend(_run_l1(skill_dir))

    failures = [r for r in results if not r.passed]
    passes = [r for r in results if r.passed]
    return failures, passes


def _run_l0(skill_dir: Path) -> list[TestResult]:
    out: list[TestResult] = []

    errors = validate_skill_dir(skill_dir)
    out.append(
        TestResult(
            "L0.validate",
            not errors,
            "; ".join(errors) if errors else "SKILL.md valid",
        )
    )

    ir_file = skill_dir / "references" / "ir.md"
    if ir_file.exists():
        try:
            compile_skill(ir_file.read_text(encoding="utf-8"), skill_dir.name)
            out.append(TestResult("L0.compile", True, "IR compiles"))
        except Exception as exc:
            out.append(TestResult("L0.compile", False, str(exc)))

        drift = check_drift(skill_dir)
        out.append(
            TestResult(
                "L0.sync",
                not drift.drifted,
                drift.message,
            )
        )
    else:
        out.append(TestResult("L0.ir", False, "missing references/ir.md"))

    skill_md = _read_skill_md(skill_dir)
    if skill_md:
        out.append(
            TestResult(
                "L0.no-todo",
                "TODO" not in skill_md and "PLACEHOLDER" not in skill_md,
                "no TODO/PLACEHOLDER in SKILL.md",
            )
        )
        fm, body = _split_frontmatter(skill_md)
        desc = str(fm.get("description", ""))
        out.append(
            TestResult(
                "L0.description",
                len(desc) >= 20 and "TODO" not in desc,
                "description present and meaningful",
            )
        )
        out.append(
            TestResult(
                "L0.failure-modes",
                body.lower().count("failure") >= 1 or re.search(r"\bF[1-9]\b", body) is not None,
                "failure modes documented",
            )
        )

    doc = parse_ir(ir_file.read_text(encoding="utf-8"), skill_dir.name) if ir_file.exists() else None
    if doc:
        failures = doc.failure_modes()
        out.append(
            TestResult(
                "L0.ir-failures",
                len(failures) >= 3,
                f"{len(failures)} failure modes in IR (need ≥3)",
            )
        )
        steps = doc.execution_steps()
        out.append(
            TestResult(
                "L0.ir-steps",
                len(steps) >= 3,
                f"{len(steps)} execution steps in IR (need ≥3)",
            )
        )

    return out


def _run_l1(skill_dir: Path) -> list[TestResult]:
    cases = _load_test_cases(skill_dir)
    if not cases:
        return [
            TestResult(
                "L1.cases",
                False,
                "no L1 cases — add references/eval.yaml or §9 tests in ir.md",
            )
        ]

    skill_md = _read_skill_md(skill_dir)
    if not skill_md:
        return [TestResult("L1.skill-md", False, "SKILL.md missing")]

    _, body = _split_frontmatter(skill_md)
    body_lower = body.lower()
    out: list[TestResult] = []

    for case in cases:
        ok = True
        msgs: list[str] = []

        for needle in case.assert_contains:
            if needle.lower() not in body_lower:
                ok = False
                msgs.append(f"missing '{needle}'")

        for section in case.assert_sections:
            if f"## {section}".lower() not in body_lower and f"# {section}".lower() not in body_lower:
                ok = False
                msgs.append(f"missing section '{section}'")

        for bad in case.assert_not_contains:
            if bad.lower() in body_lower:
                ok = False
                msgs.append(f"should not contain '{bad}'")

        out.append(
            TestResult(
                case.id,
                ok,
                case.description or "; ".join(msgs) or "ok",
            )
        )

    return out


def _load_test_cases(skill_dir: Path) -> list[TestCase]:
    yaml_file = skill_dir / "references" / "eval.yaml"
    if yaml_file.exists() and yaml is not None:
        data = yaml.safe_load(yaml_file.read_text(encoding="utf-8")) or {}
        return _cases_from_yaml(data)

    eval_md = skill_dir / "references" / "eval.md"
    if eval_md.exists():
        cases = _cases_from_eval_md(eval_md.read_text(encoding="utf-8"))
        if cases:
            return cases

    ir_file = skill_dir / "references" / "ir.md"
    if ir_file.exists():
        doc = parse_ir(ir_file.read_text(encoding="utf-8"), skill_dir.name)
        return _cases_from_ir_l1(doc.l1_tests())

    return []


def _cases_from_yaml(data: dict) -> list[TestCase]:
    cases: list[TestCase] = []
    for item in data.get("tests", []):
        asserts = item.get("assert", {})
        cases.append(
            TestCase(
                id=str(item.get("id", f"T{len(cases)+1}")),
                description=str(item.get("description", "")),
                assert_contains=[str(x) for x in asserts.get("contains", [])],
                assert_sections=[str(x) for x in asserts.get("sections", [])],
                assert_not_contains=[str(x) for x in asserts.get("not_contains", [])],
            )
        )
    return cases


def _cases_from_eval_md(text: str) -> list[TestCase]:
    cases: list[TestCase] = []
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        if "---" in line or "ID" in line and "Expected" in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        tid, inp, expected = cells[0], cells[1], cells[2]
        if not re.match(r"T\d+", tid, re.I):
            continue
        needles = _keywords_from_expected(expected, inp)
        cases.append(
            TestCase(
                id=tid,
                description=f"{inp} → {expected}",
                assert_contains=needles,
            )
        )
    return cases


def _cases_from_ir_l1(lines: list[str]) -> list[TestCase]:
    cases: list[TestCase] = []
    for i, line in enumerate(lines, 1):
        tid = f"T{i}"
        inp, expected = line, ""
        if "→" in line:
            parts = line.split("→", 1)
            inp, expected = parts[0].strip(), parts[1].strip()
        elif ":" in line and "Test" in line[:10]:
            _, rest = line.split(":", 1)
            line = rest.strip()
            if "→" in line:
                inp, expected = line.split("→", 1)
            else:
                expected = line
        needles = _keywords_from_expected(expected, inp)
        cases.append(
            TestCase(
                id=tid,
                description=line,
                assert_contains=needles,
            )
        )
    return cases


def _keywords_from_expected(expected: str, inp: str = "") -> list[str]:
    text = f"{expected} {inp}".lower()
    needles: list[str] = []

    patterns = [
        (r"\bask\b", "ASK"),
        (r"\bstage\b", "git add"),
        (r"\bfeat\b", "feat"),
        (r"\bdocs\b", "docs"),
        (r"\bsecurity\b", "security"),
        (r"\bcritical\b", "Critical"),
        (r"\breadme\b", "README"),
        (r"\btitle\b", "title"),
        (r"\bpr\b", "pr"),
        (r"\bempty\b", "empty"),
        (r"\bmanual\b", "manual"),
    ]
    for regex, token in patterns:
        if re.search(regex, text):
            needles.append(token)

    if not needles and expected:
        words = [w for w in re.findall(r"[a-zA-Z]{4,}", expected) if w.lower() not in ("test", "with", "only")]
        needles.extend(words[:3])

    return list(dict.fromkeys(needles))


def _read_skill_md(skill_dir: Path) -> str:
    path = skill_dir / "SKILL.md"
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    if yaml is None:
        return {}, parts[2]
    data = yaml.safe_load(parts[1]) or {}
    return data if isinstance(data, dict) else {}, parts[2]
