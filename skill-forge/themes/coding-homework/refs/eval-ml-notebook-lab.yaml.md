# MD 兼容视图 — `eval-ml-notebook-lab.yaml`

> **权威源文件**：同目录 `eval-ml-notebook-lab.yaml`（本文件由 `skill-core` 自动生成，请勿手改；改源文件后重新 `batch build` 或运行 compat 同步。）

| 项 | 值 |
|----|-----|
| 类型 | `yaml` |
| 路径 | `refs/eval-ml-notebook-lab.yaml` |
| 用途 | Skill 编译测试断言（eval）；CI `batch build --test` 读取 YAML 源文件。 |

## 内容

```yaml
tests:
  - id: T1
    description: ml lab
    assert:
      contains: ["ml-notebook-guide", "jupyter", "sklearn"]
      sections: ["Quick Start", "Workflow", "Failure Modes"]

  - id: T2
    description: reproducibility
    assert:
      contains: ["random seed", "requirements.txt", "outputs/figures"]

  - id: T3
    description: metrics ethics
    assert:
      contains: ["leakage", "jupyter"]

  - id: T4
    description: notebook
    assert:
      contains: ["lab_task", "pandas", "sklearn"]
```
