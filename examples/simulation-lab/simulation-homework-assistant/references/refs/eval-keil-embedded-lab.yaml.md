# MD 兼容视图 — `eval-keil-embedded-lab.yaml`

> **权威源文件**：同目录 `eval-keil-embedded-lab.yaml`（本文件由 `skill-core` 自动生成，请勿手改；改源文件后重新 `batch build` 或运行 compat 同步。）

| 项 | 值 |
|----|-----|
| 类型 | `yaml` |
| 路径 | `refs/eval-keil-embedded-lab.yaml` |
| 用途 | Skill 编译测试断言（eval）；CI `batch build --test` 读取 YAML 源文件。 |

## 内容

```yaml
tests:
  - id: T1
    description: keil workflow
    assert:
      contains: ["keil-setup", "check_keil", "mcu-devices.yaml", "pin-map"]
      sections: ["Quick Start", "Workflow", "Failure Modes"]

  - id: T2
    description: build
    assert:
      contains: ["uvprojx", "build.log", "0 Error"]

  - id: T3
    description: mcu accuracy
    assert:
      contains: ["wrong MCU selected", "STM32", "KEIL_NOT_FOUND"]

  - id: T4
    description: integrity
    assert:
      contains: ["fake 0 errors", "lab_task"]
```
