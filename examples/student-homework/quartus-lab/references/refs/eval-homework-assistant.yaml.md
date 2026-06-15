# MD 兼容视图 — `eval-homework-assistant.yaml`

> **权威源文件**：同目录 `eval-homework-assistant.yaml`（本文件由 `skill-core` 自动生成，请勿手改；改源文件后重新 `batch build` 或运行 compat 同步。）

| 项 | 值 |
|----|-----|
| 类型 | `yaml` |
| 路径 | `refs/eval-homework-assistant.yaml` |
| 用途 | Skill 编译测试断言（eval）；CI `batch build --test` 读取 YAML 源文件。 |

## 内容

```yaml
tests:
  - id: T1
    description: unified STEM router
    assert:
      contains: ["assignment-catalog.yaml", "matlab-simulink-lab", "session.yaml", "stem-tool-matrix"]
      sections: ["Quick Start", "Workflow", "Failure Modes"]

  - id: T2
    description: confirm before install
    assert:
      contains: ["confirm", "install", "quartus-lab", "routing-rules", "universal-stem-workflow"]

  - id: T3
    description: accurate scoring and planned tools
    assert:
      contains: ["min_score", "tie_threshold", "major_weight", "status planned", "stem-universal-fallback"]

  - id: T4
    description: install and handoff all themes
    assert:
      contains: ["resolve_order", "simulation-lab", "coding-homework", "HANDOFF", "block install"]
```
