#!/usr/bin/env python3
"""Backward-compatible wrapper for skill validate."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib.validate import validate_skill_dir  # noqa: E402


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python validate_skill.py <skill-directory>", file=sys.stderr)
        return 2
    skill_dir = Path(sys.argv[1]).resolve()
    errors = validate_skill_dir(skill_dir)
    if errors:
        print(f"FAIL: {skill_dir.name}")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"OK: {skill_dir.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
