#!/usr/bin/env python3
"""Detect MATLAB installation."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


def find_matlab() -> Path | None:
    found = shutil.which("matlab") or shutil.which("matlab.exe")
    if found:
        return Path(found)
    if sys.platform == "win32":
        for base in (Path(r"C:\Program Files\MATLAB"), Path(r"C:\Program Files (x86)\MATLAB")):
            if not base.is_dir():
                continue
            for ver in sorted(base.iterdir(), reverse=True):
                cand = ver / "bin" / "matlab.exe"
                if cand.is_file():
                    return cand
    return None


def main() -> int:
    exe = find_matlab()
    if exe is None:
        print("MATLAB_NOT_FOUND")
        return 1
    print(f"MATLAB_PATH={exe}")
    try:
        proc = subprocess.run(
            [str(exe), "-batch", "fprintf('%s\\n', version);"],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        out = (proc.stdout or proc.stderr or "").strip()
        if out:
            print(out)
    except subprocess.TimeoutExpired:
        print("MATLAB_VERSION=timeout")
    except OSError as exc:
        print(f"MATLAB_ERROR={exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
