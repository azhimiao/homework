---
name: python-lab
profile: hybrid
status: stable
version: "1.0.0"
invocation: auto
host: any
---

# Goal
Complete Python coursework: verify Python env, scaffold project per PEP 8, implement assignment, tests, README, report draft.

# Context
After coding-homework-assistant routes Python 程设. Triggers: "Python作业", ".py", "pytest", "Flask 作业".

# Constraints
- 精度：follow python-standards.md; real run before claim success
- 诚信：author must understand submitted code

# Inputs
## Required
- lab_task: string

## Optional
- python_version, project_path, handout

# Outputs
**Profile:** hybrid

1. Source under `homework/python-homework/{project}/`
2. `requirements.txt`, `README.md`
3. `tests/` if required
4. `docs/report.md` draft

# Steps
1. READ refs/python-standards.md
2. RUN scripts/check_python.py; IF PYTHON_NOT_FOUND → guide install; STOP
3. ASK lab_task; READ handout
4. CREATE project structure src/ tests/ docs/
5. IMPLEMENT solution; PEP 8; WRITE requirements.txt
6. RUN tests or manual cases; CAPTURE output for report
7. WRITE README with run commands
8. DRAFT docs/report.md; SYNC homework/checklist.md

# Decision
IF lab_task vague → ASK handout
IF tests fail → fix before delivery
IF user wants exam-only answer without learning → refuse integrity (F4)

# Tools
- shell — python, pytest, pip
- file_read, file_write, ask_user

# Failures
F1: python-missing | PYTHON_NOT_FOUND | install Python 3.10+
F2: test-fail | pytest fail | fix code
F3: vague-task | no spec | ask handout
F4: integrity-violation | cheat request | refuse

# Deps
depends_on:
  - skill-core
  - coding-homework-assistant
provides:
  - python-coursework

# Version
version: "1.0.0"
status: stable
