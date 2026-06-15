# MD 兼容视图 — `eval-multisim-lab.yaml`

> **权威源文件**：同目录 `eval-multisim-lab.yaml`（本文件由 `skill-core` 自动生成，请勿手改；改源文件后重新 `batch build` 或运行 compat 同步。）

| 项 | 值 |
|----|-----|
| 类型 | `yaml` |
| 路径 | `refs/eval-multisim-lab.yaml` |
| 用途 | Skill 编译测试断言（eval）；CI `batch build --test` 读取 YAML 源文件。 |

## 内容

```yaml
tests:
  - id: T1
    description: multisim workflow
    assert:
      contains: ["multisim-setup", "check_multisim", "components.md"]
      sections: ["Quick Start", "Workflow", "Failure Modes"]

  - id: T2
    description: circuit sim
    assert:
      contains: ["outputs/waveforms", "ground", "report.md"]

  - id: T3
    description: failures
    assert:
      contains: ["MULTISIM_NOT_FOUND", "fabricated waveform"]

  - id: T4
    description: handoff
    assert:
      contains: ["lab_task", "homework-assistant"]
```
