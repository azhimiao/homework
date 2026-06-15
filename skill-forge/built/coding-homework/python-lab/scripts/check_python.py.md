# MD 兼容视图 — `check_python.py`

> **权威源文件**：同目录 `check_python.py`（本文件由 `skill-core` 自动生成，请勿手改；改源文件后重新 `batch build` 或运行 compat 同步。）

| 项 | 值 |
|----|-----|
| 类型 | `py` |
| 路径 | `scripts/check_python.py` |
| 用途 | 环境检测脚本；skill Steps 中 `RUN scripts/…`。 |

## 内容

```python
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
```

## 运行

```bash
python scripts/check_python.py
```

Skill Steps 引用路径：`scripts/check_python.py` 或 `refs/scripts/check_python.py`（编译后位于 `references/refs/`）。
