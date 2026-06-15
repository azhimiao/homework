"""Export IR to JSON and JSON Schema for tooling."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .ir_parser import IRDocument, parse_ir


def ir_to_dict(doc: IRDocument) -> dict[str, Any]:
    return {
        "$schema": "skill-protocol/v2/ir",
        "skill_name": doc.skill_name,
        "compile_target": doc.compile_target(),
        "intent": {
            "goal": doc.goal(),
            "context": doc.context(),
            "constraints": doc.constraints(),
        },
        "inputs": {
            "required": doc.required_inputs(),
            "optional": doc.optional_inputs(),
        },
        "outputs": {"profile": doc.output_profile()},
        "decomposition": doc.sub_skills(),
        "execution_plan": doc.execution_steps(),
        "decision_logic": doc.decision_logic(),
        "tools": doc.tools_table(),
        "failure_modes": doc.failure_modes(),
        "l1_tests": doc.l1_tests(),
        "dependencies": doc.yaml_block(12),
        "versioning": doc.version_info(),
    }


def export_ir_json(skill_dir: Path, out_path: Path | None = None) -> Path:
    ir_file = skill_dir / "references" / "ir.md"
    if not ir_file.exists():
        raise FileNotFoundError(f"IR not found: {ir_file}")
    doc = parse_ir(ir_file.read_text(encoding="utf-8"), skill_dir.name)
    data = ir_to_dict(doc)
    target = out_path or skill_dir / "references" / "ir.json"
    target.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return target


SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schema" / "ir.schema.json"
