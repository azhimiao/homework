#!/usr/bin/env python3
"""Detect Keil uVision / ARM compiler."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path


def find_keil() -> Path | None:
    for name in ("UV4.exe", "uvision.exe"):
        found = shutil.which(name)
        if found:
            return Path(found)
    if sys.platform == "win32":
        for base in (
            Path(r"C:\Keil_v5\UV4"),
            Path(r"C:\Keil\UV4"),
            Path(r"C:\Program Files\Keil_v5\UV4"),
        ):
            exe = base / "UV4.exe"
            if exe.is_file():
                return exe
    return None


def main() -> int:
    exe = find_keil()
    if exe is None:
        print("KEIL_NOT_FOUND")
        print("Install Keil MDK-ARM (uVision5).")
        return 1
    print(f"KEIL_PATH={exe}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
