---
name: ml-notebook-lab
profile: hybrid
status: stable
version: "1.0.0"
invocation: auto
host: any
---

# Goal
Complete ML/data analysis coursework: notebook or script pipeline, reproducible metrics, figures, report.

# Context
机器学习课设, jupyter, sklearn, 数据分析. Triggers: "ML作业", "notebook", "pandas", "课设".

# Constraints
- 精度：ml-notebook-guide.md; no fabricated metrics
- 数据：no unauthorized private datasets

# Inputs
## Required
- lab_task: string

## Optional
- dataset_path, project_path, handout, use_notebook: boolean

# Outputs
**Profile:** hybrid

1. `notebooks/` or `src/train.py`
2. `requirements.txt`, `outputs/figures/`
3. `docs/report.md` with metrics

# Steps
1. READ refs/ml-notebook-guide.md
2. RUN check_python.py; pip install jupyter sklearn pandas if needed
3. ASK lab_task, dataset, metric; READ handout
4. CREATE notebook pipeline: load split train evaluate
5. CREATE src/train.py or notebook; WRITE requirements.txt
6. SET random seed; LOG hyperparams in notebook/markdown
7. SAVE figures to outputs/figures/
8. WRITE report: data, method, results, error analysis
9. UPDATE checklist

# Decision
IF dataset missing → ASK path or public sample (iris/titanic teaching only if allowed)
IF metrics too good → sanity check leakage
IF fake loss curve → forbidden

# Tools
- shell — jupyter, python
- file_read, file_write, ask_user

# Failures
F1: python-missing | no env | install
F2: metric-invalid | leakage suspected | fix split
F3: vague-task | no target metric | ask handout
F4: integrity-violation | fake results | refuse

# Deps
depends_on:
  - skill-core
  - coding-homework-assistant
provides:
  - ml-notebook-lab

# Version
version: "1.0.0"
status: stable
