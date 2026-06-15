---
name: ml-notebook-lab
description: >-
  Complete ML/data analysis coursework: notebook or script pipeline, reproducible metrics,
  figures, report. Use when 机器学习课设, jupyter, sklearn, 数据分析. Triggers: "ML作业", "notebook",
  "pandas", "课设".
metadata:
  version: "1.0.0"
  status: stable
  protocol: skill-protocol-v2
---

# Ml Notebook Lab

## Quick Start

1. READ refs/ml-notebook-guide.md
2. RUN check_python.py; pip install jupyter sklearn pandas if needed
3. ASK lab_task, dataset, metric; READ handout
4. CREATE notebook pipeline: load split train evaluate
5. CREATE src/train.py or notebook; WRITE requirements.txt

## Workflow

### Step 1
READ refs/ml-notebook-guide.md

### Step 2
RUN check_python.py; pip install jupyter sklearn pandas if needed

### Step 3
ASK lab_task, dataset, metric; READ handout

### Step 4
CREATE notebook pipeline: load split train evaluate

### Step 5
CREATE src/train.py or notebook; WRITE requirements.txt

### Step 6
SET random seed; LOG hyperparams in notebook/markdown

### Step 7
SAVE figures to outputs/figures/

### Step 8
WRITE report: data, method, results, error analysis

### Step 9
UPDATE checklist

### Decision logic

```
IF dataset missing → ASK path or public sample (iris/titanic teaching only if allowed)
IF metrics too good → sanity check leakage
IF fake loss curve → forbidden
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
| F1 | no env | install |
| F2 | leakage suspected | fix split |
| F3 | no target metric | ask handout |
| F4 | fake results | refuse |

## Dependencies

- `skill-core`
- `coding-homework-assistant`

## Additional Resources

- [IR source](references/ir.md)
