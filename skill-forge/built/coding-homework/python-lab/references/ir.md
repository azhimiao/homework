python-lab

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
Complete Python coursework: verify Python env, scaffold project per PEP 8, implement assignment, tests, README, report draft.

## Context
After coding-homework-assistant routes Python 程设. Triggers: "Python作业", ".py", "pytest", "Flask 作业".

## Constraints
- 精度：follow python-standards.md; real run before claim success
- 诚信：author must understand submitted code

---

# 2. Inputs（输入定义）

## Required Inputs
## Required
- lab_task: string

## Optional
- python_version, project_path, handout

---

# 3. Outputs（输出定义）

**Profile:** hybrid

1. Source under `homework/python-homework/{project}/`
2. `requirements.txt`, `README.md`
3. `tests/` if required
4. `docs/report.md` draft

---

# 5. Execution Plan（执行流程）

1. READ refs/python-standards.md
2. RUN scripts/check_python.py; IF PYTHON_NOT_FOUND → guide install; STOP
3. ASK lab_task; READ handout
4. CREATE project structure src/ tests/ docs/
5. IMPLEMENT solution; PEP 8; WRITE requirements.txt
6. RUN tests or manual cases; CAPTURE output for report
7. WRITE README with run commands
8. DRAFT docs/report.md; SYNC homework/checklist.md

---

# 6. Decision Logic（决策系统）

```
IF lab_task vague → ASK handout
IF tests fail → fix before delivery
IF user wants exam-only answer without learning → refuse integrity (F4)
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
- Signal: PYTHON_NOT_FOUND
- Recovery: install Python 3.10+
- Severity: block

## F2: test-fail
- Signal: pytest fail
- Recovery: fix code
- Severity: block

## F3: vague-task
- Signal: no spec
- Recovery: ask handout
- Severity: block

## F4: integrity-violation
- Signal: cheat request
- Recovery: refuse
- Severity: block

---

# 12. Skill Graph Dependencies（依赖）

```yaml
depends_on:
  - skill-core
  - coding-homework-assistant
provides:
  - python-coursework
```

---

# 13. Versioning（版本系统）

```yaml
version: "1.0.0"
status: stable
```
