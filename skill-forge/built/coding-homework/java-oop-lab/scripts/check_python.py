#!/usr/bin/env python3
"""Detect Python for coding homework."""

from __future__ import annotations

import shutil
import subprocess
import sys


def main() -> int:
    exe = shutil.which("python") or shutil.which("python3")
    if not exe:
        print("PYTHON_NOT_FOUND")
        return 1
    print(f"PYTHON_PATH={exe}")
    try:
        proc = subprocess.run(
            [exe, "--version"],
            capture_output=True,
            text=True,
            timeout=8,
            check=False,
        )
        print((proc.stdout or proc.stderr or "").strip())
        proc = subprocess.run(
            [exe, "-m", "pip", "--version"],
            capture_output=True,
            text=True,
            timeout=8,
            check=False,
        )
        if proc.stdout:
            print(proc.stdout.strip())
    except subprocess.TimeoutExpired:
        print("PYTHON_VERSION=timeout")
    except OSError as exc:
        print(f"PYTHON_ERROR={exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
