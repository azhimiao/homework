# MD 兼容视图 — `eval-matlab-simulink-lab.yaml`

> **权威源文件**：同目录 `eval-matlab-simulink-lab.yaml`（本文件由 `skill-core` 自动生成，请勿手改；改源文件后重新 `batch build` 或运行 compat 同步。）

| 项 | 值 |
|----|-----|
| 类型 | `yaml` |
| 路径 | `refs/eval-matlab-simulink-lab.yaml` |
| 用途 | Skill 编译测试断言（eval）；CI `batch build --test` 读取 YAML 源文件。 |

## 内容

```yaml
tests:
  - id: T1
    description: matlab workflow
    assert:
      contains: ["matlab-simulink-setup", "check_matlab", "Simulink", "params.md"]
      sections: ["Quick Start", "Workflow", "Failure Modes"]

  - id: T2
    description: outputs
    assert:
      contains: ["report-template", "outputs/figures", "report.md"]

  - id: T3
    description: failures
    assert:
      contains: ["MATLAB_NOT_FOUND", "fabricated plots"]

  - id: T4
    description: deps
    assert:
      contains: ["homework-assistant", "lab_task"]
```
