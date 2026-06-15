# MD 兼容视图 — `eval-simulation-homework-assistant.yaml`

> **权威源文件**：同目录 `eval-simulation-homework-assistant.yaml`（本文件由 `skill-core` 自动生成，请勿手改；改源文件后重新 `batch build` 或运行 compat 同步。）

| 项 | 值 |
|----|-----|
| 类型 | `yaml` |
| 路径 | `refs/eval-simulation-homework-assistant.yaml` |
| 用途 | Skill 编译测试断言（eval）；CI `batch build --test` 读取 YAML 源文件。 |

## 内容

```yaml
tests:
  - id: T1
    description: alias unified router
    assert:
      contains: ["homework-assistant", "assignment-catalog.yaml", "matlab-simulink-lab", "session.yaml"]
      sections: ["Quick Start", "Workflow", "Failure Modes"]

  - id: T2
    description: confirm install simulation labs
    assert:
      contains: ["confirm", "install", "simulation-lab", "multisim-lab", "DELEGATE"]

  - id: T3
    description: all lab skills handoff
    assert:
      contains: ["keil-embedded-lab", "HANDOFF", "checklist.md", "stem-tool-matrix"]

  - id: T4
    description: planned tool fallback
    assert:
      contains: ["universal-stem-workflow", "planned-tool", "block install"]
```
