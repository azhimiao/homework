---
name: python-lab
description: >-
  Complete Python coursework: verify Python env, scaffold project per PEP 8, implement
  assignment, tests, README, report draft. Use when after coding-homework-assistant routes
  Python 程设. Triggers: "Python作业", ".py", "pytest", "Flask 作业".
metadata:
  version: "1.0.0"
  status: stable
  protocol: skill-protocol-v2
---

# Python Lab

## Quick Start

1. READ refs/python-standards.md
2. RUN scripts/check_python.py; IF PYTHON_NOT_FOUND → guide install; STOP
3. ASK lab_task; READ handout
4. CREATE project structure src/ tests/ docs/
5. IMPLEMENT solution; PEP 8; WRITE requirements.txt

## Workflow

### Step 1
READ refs/python-standards.md

### Step 2
RUN scripts/check_python.py; IF PYTHON_NOT_FOUND → guide install; STOP

### Step 3
ASK lab_task; READ handout

### Step 4
CREATE project structure src/ tests/ docs/

### Step 5
IMPLEMENT solution; PEP 8; WRITE requirements.txt

### Step 6
RUN tests or manual cases; CAPTURE output for report

### Step 7
WRITE README with run commands

### Step 8
DRAFT docs/report.md; SYNC homework/checklist.md

### Decision logic

```
IF lab_task vague → ASK handout
IF tests fail → fix before delivery
IF user wants exam-only answer without learning → refuse integrity (F4)
```

## Outputs

Profile: `hybrid`

Return artifacts plus a narrative summary.

## Tools

| ID | Use | Constraints |
|----|-----|-------------|
| shell |  |  |
| file_read, |  |  |

## Failure Modes

| ID | Signal | Recovery |
|----|--------|----------|
| F1 | PYTHON_NOT_FOUND | install Python 3.10+ |
| F2 | pytest fail | fix code |
| F3 | no spec | ask handout |
| F4 | cheat request | refuse |

## Dependencies

- `skill-core`
- `coding-homework-assistant`

## Additional Resources

- [IR source](references/ir.md)
