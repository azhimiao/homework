# MD 兼容视图 — `check_java.py`

> **权威源文件**：同目录 `check_java.py`（本文件由 `skill-core` 自动生成，请勿手改；改源文件后重新 `batch build` 或运行 compat 同步。）

| 项 | 值 |
|----|-----|
| 类型 | `py` |
| 路径 | `scripts/check_java.py` |
| 用途 | 环境检测脚本；skill Steps 中 `RUN scripts/…`。 |

## 内容

```python
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
```

## 运行

```bash
python scripts/check_java.py
```

Skill Steps 引用路径：`scripts/check_java.py` 或 `refs/scripts/check_java.py`（编译后位于 `references/refs/`）。
