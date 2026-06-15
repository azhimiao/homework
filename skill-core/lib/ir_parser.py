"""Parse Skill Protocol IR markdown into structured sections."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore


SECTION_RE = re.compile(r"^#\s+(\d+)\.\s+.+$", re.MULTILINE)
SUBSECTION_RE = re.compile(r"^##\s+(.+)$", re.MULTILINE)
PLACEHOLDER_RE = re.compile(r"^<[^>]+>$")


@dataclass
class IRDocument:
    skill_name: str = ""
    sections: dict[int, str] = field(default_factory=dict)
    raw: str = ""

    def section(self, num: int) -> str:
        return self.sections.get(num, "").strip()

    def subsection(self, num: int, title: str) -> str:
        body = self.section(num)
        pattern = re.compile(
            rf"^##\s+{re.escape(title)}\s*$([\s\S]*?)(?=^##\s+|\Z)",
            re.MULTILINE | re.IGNORECASE,
        )
        match = pattern.search(body)
        return match.group(1).strip() if match else ""

    def yaml_block(self, num: int) -> dict[str, Any]:
        body = self.section(num)
        match = re.search(r"```ya?ml\s*\n([\s\S]*?)```", body, re.IGNORECASE)
        if not match:
            return {}
        if yaml is None:
            return {"_raw": match.group(1)}
        data = yaml.safe_load(match.group(1))
        return data if isinstance(data, dict) else {}

    def fenced_block(self, num: int, lang: str | None = None) -> str:
        body = self.section(num)
        if lang:
            match = re.search(rf"```{lang}\s*\n([\s\S]*?)```", body, re.IGNORECASE)
        else:
            match = re.search(r"```\s*\n([\s\S]*?)```", body)
        return match.group(1).strip() if match else ""

    def goal(self) -> str:
        text = self.subsection(1, "Goal")
        return _first_meaningful_line(text)

    def context(self) -> str:
        text = self.subsection(1, "Context")
        return _clean_prose(text)

    def constraints(self) -> list[str]:
        body = self.section(1)
        match = re.search(r"^##\s+Constraints\s*$([\s\S]*?)(?=^##\s+|\Z)", body, re.MULTILINE | re.IGNORECASE)
        if not match:
            return []
        items = []
        for line in match.group(1).splitlines():
            line = line.strip()
            if line.startswith("- "):
                item = line[2:].strip()
                if not _is_placeholder(item):
                    items.append(item)
        return items

    def output_profile(self) -> str:
        body = self.section(3)
        match = re.search(r"\*\*Profile:\*\*\s*(\w+)", body, re.IGNORECASE)
        if match:
            return match.group(1).lower()
        match = re.search(r"Profile:\s*(\w+)", body, re.IGNORECASE)
        return match.group(1).lower() if match else "narrative"

    def execution_steps(self) -> list[str]:
        body = self.section(5)
        steps = []
        for line in body.splitlines():
            line = line.strip()
            m = re.match(r"^\d+\.\s+(.+)$", line)
            if m and not line.startswith("<!--"):
                step = m.group(1).strip()
                if not _is_placeholder(step.replace("…", "").replace("...", "")):
                    steps.append(step)
        return steps

    def decision_logic(self) -> str:
        return self.fenced_block(6) or self.section(6)

    def failure_modes(self) -> list[dict[str, str]]:
        body = self.section(10)
        modes: list[dict[str, str]] = []
        for match in re.finditer(
            r"^##\s+(F\d+):\s*(.+)$([\s\S]*?)(?=^##\s+F\d+:|^##\s+|\Z)",
            body,
            re.MULTILINE,
        ):
            fid, name, block = match.group(1), match.group(2).strip(), match.group(3)
            modes.append(
                {
                    "id": fid,
                    "name": name,
                    "signal": _field(block, "Signal"),
                    "recovery": _field(block, "Recovery"),
                    "severity": _field(block, "Severity"),
                }
            )
        return modes

    def tools_table(self) -> list[dict[str, str]]:
        body = self.section(7)
        rows: list[dict[str, str]] = []
        in_table = False
        for line in body.splitlines():
            if line.strip().startswith("|") and "Portable ID" in line:
                in_table = True
                continue
            if in_table and line.strip().startswith("|") and "---" in line:
                continue
            if in_table and line.strip().startswith("|"):
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cells) >= 2 and cells[0] and cells[0] != "Portable ID":
                    if not _is_placeholder(cells[0]):
                        rows.append(
                            {
                                "id": cells[0],
                                "use": cells[1] if len(cells) > 1 else "",
                                "constraints": cells[2] if len(cells) > 2 else "",
                            }
                        )
            elif in_table and line.strip() and not line.strip().startswith("|"):
                break
        return rows

    def sub_skills(self) -> list[dict[str, str]]:
        body = self.section(4)
        subs: list[dict[str, str]] = []
        for match in re.finditer(r"^##\s+(S\d+):\s*(.+)$([\s\S]*?)(?=^##\s+S\d+:|^##\s+|\Z)", body, re.MULTILINE):
            sid, name, block = match.group(1), match.group(2).strip(), match.group(3)
            if _is_placeholder(name):
                continue
            subs.append(
                {
                    "id": sid,
                    "name": name,
                    "goal": _field(block, "Goal"),
                    "inputs": _field(block, "Inputs"),
                    "outputs": _field(block, "Outputs"),
                    "verb": _field(block, "Primary verb"),
                }
            )
        return subs

    def l1_tests(self) -> list[str]:
        body = self.subsection(9, "L1 Task (before stable)") or self.subsection(9, "L1 Task")
        tests = []
        for line in body.splitlines():
            line = line.strip()
            if line.startswith("- Test") or line.startswith("- T"):
                if not _is_placeholder(line):
                    tests.append(line.lstrip("- ").strip())
        return tests

    def required_inputs(self) -> list[str]:
        body = self.subsection(2, "Required Inputs")
        items = []
        for line in body.splitlines():
            line = line.strip()
            if line.startswith("- ") and not _is_placeholder(line[2:]):
                items.append(line[2:].strip())
        return items

    def optional_inputs(self) -> list[str]:
        body = self.subsection(2, "Optional Inputs")
        items = []
        for line in body.splitlines():
            line = line.strip()
            if line.startswith("- ") and not _is_placeholder(line[2:]):
                items.append(line[2:].strip())
        return items

    def version_info(self) -> dict[str, Any]:
        return self.yaml_block(13)

    def compile_target(self) -> dict[str, Any]:
        return self.yaml_block(0)


def parse_ir(text: str, skill_name: str = "") -> IRDocument:
    name = skill_name
    first_line = text.splitlines()[0] if text.splitlines() else ""
    if not name:
        for i, line in enumerate(text.splitlines()[:6]):
            if line.strip() and not line.startswith("#") and not line.startswith("<!--"):
                candidate = line.strip()
                if not PLACEHOLDER_RE.match(candidate):
                    name = candidate
                    break

    sections: dict[int, str] = {}
    matches = list(SECTION_RE.finditer(text))
    for i, match in enumerate(matches):
        num = int(match.group(1))
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[num] = text[start:end].strip()

    return IRDocument(skill_name=name, sections=sections, raw=text)


def _field(block: str, label: str) -> str:
    match = re.search(rf"^-\s+{label}:\s*(.*)$", block, re.MULTILINE | re.IGNORECASE)
    if not match:
        return ""
    value = match.group(1).strip()
    return "" if _is_placeholder(value) else value


def _first_meaningful_line(text: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line and not _is_placeholder(line):
            return line
    return ""


def _clean_prose(text: str) -> str:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip() and not _is_placeholder(ln.strip())]
    return " ".join(lines)


def _is_placeholder(value: str) -> bool:
    value = value.strip()
    if not value:
        return True
    if PLACEHOLDER_RE.match(value):
        return True
    if value in ("…", "...", "TODO", "TODO."):
        return True
    if value.startswith("<") and value.endswith(">"):
        return True
    return False
