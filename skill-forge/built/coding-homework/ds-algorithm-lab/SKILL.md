---
name: ds-algorithm-lab
description: >-
  Complete data structures / algorithms lab: implement algorithm, complexity analysis,
  tests, report. Use when 数据结构实验, 算法作业, 链表/树/图. Triggers: "数据结构", "算法实验", "复杂度".
metadata:
  version: "1.0.0"
  status: stable
  protocol: skill-protocol-v2
---

# Ds Algorithm Lab

## Quick Start

1. READ refs/ds-algorithms-guide.md
2. RUN check_python.py if Python else check_java.py
3. ASK lab_task and algorithm spec; READ handout
4. IMPLEMENT with clear API; WRITE tests
5. RUN pytest or handout cases; all pass

## Workflow

### Step 1
READ refs/ds-algorithms-guide.md

### Step 2
RUN check_python.py if Python else check_java.py

### Step 3
ASK lab_task and algorithm spec; READ handout

### Step 4
IMPLEMENT with clear API; WRITE tests

### Step 5
RUN pytest or handout cases; all pass

### Step 6
WRITE docs/complexity.md — O time/space

### Step 7
DRAFT report; UPDATE checklist

### Decision logic

```
IF handout gives Java → switch toolchain
IF wrong complexity → revise before delivery
IF only paste LeetCode without local run → require local tests
```

## Outputs

Profile: `hybrid`

Return artifacts plus a narrative summary.

## Tools

| ID | Use | Constraints |
|----|-----|-------------|
| shell, |  |  |

## Failure Modes

| ID | Signal | Recovery |
|----|--------|----------|
| F1 | no python/java | install |
| F2 | cases fail | fix algorithm |
| F3 | no O() doc | add complexity.md |
| F4 | cheat | refuse |

## Dependencies

- `skill-core`
- `coding-homework-assistant`

## Additional Resources

- [IR source](references/ir.md)
