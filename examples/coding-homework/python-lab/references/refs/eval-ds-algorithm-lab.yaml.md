# MD 兼容视图 — `eval-ds-algorithm-lab.yaml`

> **权威源文件**：同目录 `eval-ds-algorithm-lab.yaml`（本文件由 `skill-core` 自动生成，请勿手改；改源文件后重新 `batch build` 或运行 compat 同步。）

| 项 | 值 |
|----|-----|
| 类型 | `yaml` |
| 路径 | `refs/eval-ds-algorithm-lab.yaml` |
| 用途 | Skill 编译测试断言（eval）；CI `batch build --test` 读取 YAML 源文件。 |

## 内容

```yaml
tests:
  - id: T1
    description: ds lab
    assert:
      contains: ["ds-algorithms-guide", "complexity", "pytest"]
      sections: ["Quick Start", "Workflow", "Failure Modes"]

  - id: T2
    description: algorithm
    assert:
      contains: ["complexity.md", "ds-algorithms-guide", "pytest"]

  - id: T3
    description: toolchain
    assert:
      contains: ["check_python", "no python/java"]

  - id: T4
    description: integrity
    assert:
      contains: ["LeetCode", "cheat"]
```
