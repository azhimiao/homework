# MD 兼容索引 — 理工科作业（student-homework）

纯 Markdown 环境（如 `skill/` 包、无 YAML 解析）请读 **`*.yaml.md` / `*.py.md`**，勿读无 `.md` 后缀的源文件。

| 权威源 | MD 镜像 | 用途 |
|--------|---------|------|
| `refs/assignment-catalog.yaml` | `assignment-catalog.yaml.md` | **v3 统一路由**（FPGA+编程+仿真+planned 工科） |
| `refs/session-schema.yaml` | `session-schema.yaml.md` | `homework/session.yaml` 字段 |
| `refs/board-devices.yaml` | `board-devices.yaml.md` | 板卡 → FPGA 器件 |
| `refs/eval-homework-assistant.yaml` | `eval-homework-assistant.yaml.md` | CI 断言 |
| `refs/eval-quartus-lab.yaml` | `eval-quartus-lab.yaml.md` | CI 断言 |
| `scripts/check_quartus.py` | `scripts/check_quartus.py.md` | Quartus 环境检测 |

已是 `.md` 的手写文档（无镜像）：`routing-rules.md`、`stem-tool-matrix.md`、`universal-stem-workflow.md`、`checklist-template.md`、`quartus-setup.md`、`board-pins/*.md`

## 相关 theme（工科子 lab）

| Theme | 关键 MD 镜像 |
|-------|----------------|
| `coding-homework` | `refs/assignment-catalog.yaml.md`，`scripts/check_python.py.md`，`check_java.py.md` |
| `simulation-lab` | `refs/assignment-catalog.yaml.md`，`mcu-devices.yaml.md`，`check_matlab.py.md` 等 |

编译后路径：`examples/homework-assistant/references/refs/*.yaml.md`

## 同步

```bash
python skill-core/skill.py batch compat student-homework
python skill-core/skill.py batch build student-homework --test
```
