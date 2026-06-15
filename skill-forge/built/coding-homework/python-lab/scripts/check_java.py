#!/usr/bin/env python3
"""Detect Java JDK for coding homework."""

from __future__ import annotations

import shutil
import subprocess
import sys


def main() -> int:
    java = shutil.which("java")
    javac = shutil.which("javac")
    if not java or not javac:
        print("JAVA_NOT_FOUND")
        return 1
    print(f"JAVA_PATH={java}")
    print(f"JAVAC_PATH={javac}")
    for cmd in ([java, "-version"],):
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=8,
                check=False,
            )
            print((proc.stderr or proc.stdout or "").strip())
        except subprocess.TimeoutExpired:
            print("JAVA_VERSION=timeout")
        except OSError as exc:
            print(f"JAVA_ERROR={exc}")
            return 1
    mvn = shutil.which("mvn")
    if mvn:
        print(f"MVN_PATH={mvn}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
