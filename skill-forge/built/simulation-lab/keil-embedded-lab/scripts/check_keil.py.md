# MD 兼容视图 — `check_keil.py`

> **权威源文件**：同目录 `check_keil.py`（本文件由 `skill-core` 自动生成，请勿手改；改源文件后重新 `batch build` 或运行 compat 同步。）

| 项 | 值 |
|----|-----|
| 类型 | `py` |
| 路径 | `scripts/check_keil.py` |
| 用途 | 环境检测脚本；skill Steps 中 `RUN scripts/…`。 |

## 内容

```python
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
```

## 运行

```bash
python scripts/check_keil.py
```

Skill Steps 引用路径：`scripts/check_keil.py` 或 `refs/scripts/check_keil.py`（编译后位于 `references/refs/`）。
