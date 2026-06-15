ml-notebook-lab

---

# 0. Compilation Target

```yaml
host: any
invocation: auto
output_profile: hybrid
```

---

# 1. Intent（意图）

Theme: coding-homework

## Goal
Complete ML/data analysis coursework: notebook or script pipeline, reproducible metrics, figures, report.

## Context
机器学习课设, jupyter, sklearn, 数据分析. Triggers: "ML作业", "notebook", "pandas", "课设".

## Constraints
- 精度：ml-notebook-guide.md; no fabricated metrics
- 数据：no unauthorized private datasets

---

# 2. Inputs（输入定义）

## Required Inputs
## Required
- lab_task: string

## Optional
- dataset_path, project_path, handout, use_notebook: boolean

---

# 3. Outputs（输出定义）

**Profile:** hybrid

1. `notebooks/` or `src/train.py`
2. `requirements.txt`, `outputs/figures/`
3. `docs/report.md` with metrics

---

# 5. Execution Plan（执行流程）

1. READ refs/ml-notebook-guide.md
2. RUN check_python.py; pip install jupyter sklearn pandas if needed
3. ASK lab_task, dataset, metric; READ handout
4. CREATE notebook pipeline: load split train evaluate
5. CREATE src/train.py or notebook; WRITE requirements.txt
6. SET random seed; LOG hyperparams in notebook/markdown
7. SAVE figures to outputs/figures/
8. WRITE report: data, method, results, error analysis
9. UPDATE checklist

---

# 6. Decision Logic（决策系统）

```
IF dataset missing → ASK path or public sample (iris/titanic teaching only if allowed)
IF metrics too good → sanity check leakage
IF fake loss curve → forbidden
```

---

# 7. Tool / API Binding（工具绑定）

| Portable ID | Use | Constraints |
|-------------|-----|-------------|
| shell | | |
| file_read, | | |

---

# 10. Failure Modes（失败模式）

## F1: python-missing
- Signal: no env
- Recovery: install
- Severity: block

## F2: metric-invalid
- Signal: leakage suspected
- Recovery: fix split
- Severity: block

## F3: vague-task
- Signal: no target metric
- Recovery: ask handout
- Severity: block

## F4: integrity-violation
- Signal: fake results
- Recovery: refuse
- Severity: block

---

# 12. Skill Graph Dependencies（依赖）

```yaml
depends_on:
  - skill-core
  - coding-homework-assistant
provides:
  - ml-notebook-lab
```

---

# 13. Versioning（版本系统）

```yaml
version: "1.0.0"
status: stable
```
