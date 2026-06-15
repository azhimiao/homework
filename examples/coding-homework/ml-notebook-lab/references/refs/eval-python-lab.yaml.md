# MD 兼容视图 — `eval-python-lab.yaml`

> **权威源文件**：同目录 `eval-python-lab.yaml`（本文件由 `skill-core` 自动生成，请勿手改；改源文件后重新 `batch build` 或运行 compat 同步。）

| 项 | 值 |
|----|-----|
| 类型 | `yaml` |
| 路径 | `refs/eval-python-lab.yaml` |
| 用途 | Skill 编译测试断言（eval）；CI `batch build --test` 读取 YAML 源文件。 |

## 内容

```yaml
tests:
  - id: T1
    description: python lab workflow
    assert:
      contains: ["python-standards", "check_python", "PEP 8", "pytest"]
      sections: ["Quick Start", "Workflow", "Failure Modes"]

  - id: T2
    description: outputs
    assert:
      contains: ["requirements.txt", "README", "report.md"]

  - id: T3
    description: integrity
    assert:
      contains: ["integrity", "PYTHON_NOT_FOUND"]

  - id: T4
    description: handoff context
    assert:
      contains: ["coding-homework-assistant", "lab_task"]
```
