# MD 兼容视图 — `check_multisim.py`

> **权威源文件**：同目录 `check_multisim.py`（本文件由 `skill-core` 自动生成，请勿手改；改源文件后重新 `batch build` 或运行 compat 同步。）

| 项 | 值 |
|----|-----|
| 类型 | `py` |
| 路径 | `scripts/check_multisim.py` |
| 用途 | 环境检测脚本；skill Steps 中 `RUN scripts/…`。 |

## 内容

```python
#!/usr/bin/env python3
"""Detect NI Multisim common install paths."""

from __future__ import annotations

import sys
from pathlib import Path


def find_multisim() -> Path | None:
    candidates = []
    if sys.platform == "win32":
        for base in (
            Path(r"C:\Program Files (x86)\National Instruments\Circuit Design Suite"),
            Path(r"C:\Program Files\National Instruments\Circuit Design Suite"),
        ):
            if not base.is_dir():
                continue
            for ver in sorted(base.iterdir(), reverse=True):
                exe = ver / "multisim.exe"
                if exe.is_file():
                    candidates.append(exe)
    return candidates[0] if candidates else None


def main() -> int:
    exe = find_multisim()
    if exe is None:
        print("MULTISIM_NOT_FOUND")
        print("Install NI Multisim or verify Circuit Design Suite path.")
        return 1
    print(f"MULTISIM_PATH={exe}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## 运行

```bash
python scripts/check_multisim.py
```

Skill Steps 引用路径：`scripts/check_multisim.py` 或 `refs/scripts/check_multisim.py`（编译后位于 `references/refs/`）。
