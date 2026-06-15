#!/usr/bin/env python3
"""Backward-compatible wrapper for skill init."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib.scaffold import scaffold  # noqa: E402

DEFAULT_ROOT = ROOT.parent


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python scaffold_skill.py <skill-name> [output-root]", file=sys.stderr)
        return 2
    name = sys.argv[1]
    root = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else DEFAULT_ROOT
    try:
        dest = scaffold(name, root)
    except (ValueError, FileExistsError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Created: {dest}")
    print(f"Next: skill compile {dest.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
