# MD 兼容视图 — `eval-coding-homework-assistant.yaml`

> **权威源文件**：同目录 `eval-coding-homework-assistant.yaml`（本文件由 `skill-core` 自动生成，请勿手改；改源文件后重新 `batch build` 或运行 compat 同步。）

| 项 | 值 |
|----|-----|
| 类型 | `yaml` |
| 路径 | `refs/eval-coding-homework-assistant.yaml` |
| 用途 | Skill 编译测试断言（eval）；CI `batch build --test` 读取 YAML 源文件。 |

## 内容

```yaml
tests:
  - id: T1
    description: coding router
    assert:
      contains: ["assignment-catalog.yaml", "python-lab", "session.yaml"]
      sections: ["Quick Start", "Workflow", "Failure Modes"]

  - id: T2
    description: confirm install
    assert:
      contains: ["confirm", "install", "resolve_order", "coding-homework"]

  - id: T3
    description: lab skills list
    assert:
      contains: ["java-oop-lab", "ds-algorithm-lab", "ml-notebook-lab", "academic integrity"]

  - id: T4
    description: handoff
    assert:
      contains: ["HANDOFF", "checklist.md", "block install"]
```
