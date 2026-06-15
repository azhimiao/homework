---
name: coding-homework-assistant
description: >-
  Route programming coursework: major + assignment → score coding assignment-catalog.yaml,
  confirm, auto-install python-lab / java-oop-lab / ds-algorithm-lab / ml-notebook-lab,
  handoff with checklist. Use when student says Python作业, Java实验, 数据结构, 机器学习课设. Triggers:
  "编程作业", "程设", "install python skill", "算法实验", "jupyter 作业".
metadata:
  version: "1.0.0"
  status: stable
  protocol: skill-protocol-v2
compatibility: skill-core install CLI; scope=project default
---

# Coding Homework Assistant

## Quick Start

1. ASK major, assignment; READ refs/routing-rules.md
2. READ refs/assignment-catalog.yaml; COMPUTE scores
3. IF tie or low score → ASK clarify or pick top 3
4. SHOW match; ASK confirm before install
5. WRITE homework/session.yaml; CREATE homework/{workspace_subdir}/

## Workflow

### Step 1
ASK major, assignment; READ refs/routing-rules.md

### Step 2
READ refs/assignment-catalog.yaml; COMPUTE scores

### Step 3
IF tie or low score → ASK clarify or pick top 3

### Step 4
SHOW match; ASK confirm before install

### Step 5
WRITE homework/session.yaml; CREATE homework/{workspace_subdir}/

### Step 6
RESOLVE skill per install.resolve_order (coding-homework built path); install python-lab java-oop-lab ds-algorithm-lab ml-notebook-lab as matched

### Step 7
RUN skill-core install for each skill; LOG results

### Step 8
WRITE homework/checklist.md from deliverables; ASK handout

### Step 9
HANDOFF: READ installed SKILL.md; ASK lab_task; enforce academic integrity

### Decision logic

```
IF user declines confirm → block install
IF install fails → retry built path; manual command
IF ambiguous → ask choose python vs java vs ds vs ml
IF FPGA/quartus assignment → suggest student-homework homework-assistant instead
```

## Outputs

Profile: `hybrid`

Return artifacts plus a narrative summary.

## Tools

| ID | Use | Constraints |
|----|-----|-------------|
| ask_user, |  |  |

## Failure Modes

| ID | Signal | Recovery |
|----|--------|----------|
| F1 | score below min_score | top 3 + clarify |
| F2 | CLI error | manual command |
| F3 | tie | user choose |
| F4 | user asks exam cheat | refuse; offer learning mode |
| F5 | user did not confirm | block install |

## Dependencies

- `skill-core`

## Additional Resources

- [IR source](references/ir.md)
