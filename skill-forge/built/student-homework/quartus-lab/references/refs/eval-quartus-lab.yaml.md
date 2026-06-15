# MD 兼容视图 — `eval-quartus-lab.yaml`

> **权威源文件**：同目录 `eval-quartus-lab.yaml`（本文件由 `skill-core` 自动生成，请勿手改；改源文件后重新 `batch build` 或运行 compat 同步。）

| 项 | 值 |
|----|-----|
| 类型 | `yaml` |
| 路径 | `refs/eval-quartus-lab.yaml` |
| 用途 | Skill 编译测试断言（eval）；CI `batch build --test` 读取 YAML 源文件。 |

## 内容

```yaml
tests:
  - id: T1
    description: quartus accurate workflow
    assert:
      contains: ["board-devices.yaml", "check_quartus", "Pin Planner"]
      sections: ["Quick Start", "Workflow", "Failure Modes"]

  - id: T2
    description: device accuracy
    assert:
      contains: ["10M50DAF484C7G", "MAX 10", "DE10-Lite", "wrong FPGA family"]

  - id: T3
    description: compile and verify
    assert:
      contains: ["quartus_sh", "build-log", "QUARTUS_NOT_FOUND"]

  - id: T4
    description: pins and failures
    assert:
      contains: ["pin-assignment", "conflicting pins", "handout"]
```
