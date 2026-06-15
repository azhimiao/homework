"""Entry point for pip install: skill"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def main() -> None:
    skill_py = Path(__file__).resolve().parent / "skill-core" / "skill.py"
    spec = importlib.util.spec_from_file_location("skill_core_main", skill_py)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {skill_py}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sys.exit(mod.main())


if __name__ == "__main__":
    main()
