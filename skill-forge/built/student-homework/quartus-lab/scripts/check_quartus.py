#!/usr/bin/env python3
"""Detect Intel Quartus Prime and print version. Exit 0 if found."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


def find_quartus() -> Path | None:
    for name in ("quartus", "quartus.exe"):
        found = shutil.which(name)
        if found:
            return Path(found)

    if sys.platform == "win32":
        for base in sorted(Path("C:/intelFPGA_lite").glob("*"), reverse=True):
            cand = base / "quartus" / "bin64" / "quartus.exe"
            if cand.is_file():
                return cand
        for base in sorted(Path("C:/intelFPGA").glob("*"), reverse=True):
            cand = base / "quartus" / "bin64" / "quartus.exe"
            if cand.is_file():
                return cand

    for base in (Path("/opt/intelFPGA_lite"), Path("/opt/intelFPGA")):
        if not base.is_dir():
            continue
        for ver in sorted(base.iterdir(), reverse=True):
            cand = ver / "quartus" / "bin" / "quartus"
            if cand.is_file():
                return cand
    return None


def main() -> int:
    exe = find_quartus()
    if exe is None:
        print("QUARTUS_NOT_FOUND")
        print("Install Quartus Prime Lite and MAX10/Cyclone device support.")
        return 1

    print(f"QUARTUS_PATH={exe}")
    try:
        proc = subprocess.run(
            [str(exe), "--version"],
            capture_output=True,
            text=True,
            timeout=8,
            check=False,
        )
        out = (proc.stdout or proc.stderr or "").strip()
        if out:
            print(out)
        else:
            print("QUARTUS_VERSION=unknown (binary found; --version produced no output)")
    except subprocess.TimeoutExpired:
        print("QUARTUS_VERSION=timeout (--version hung; binary exists at path above)")
    except OSError as exc:
        print(f"QUARTUS_EXEC_ERROR={exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
