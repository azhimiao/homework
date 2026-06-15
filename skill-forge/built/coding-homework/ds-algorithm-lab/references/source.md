---
name: ds-algorithm-lab
profile: hybrid
status: stable
version: "1.0.0"
invocation: auto
host: any
---

# Goal
Complete data structures / algorithms lab: implement algorithm, complexity analysis, tests, report.

# Context
数据结构实验, 算法作业, 链表/树/图. Triggers: "数据结构", "算法实验", "复杂度".

# Constraints
- 精度：ds-algorithms-guide.md; complexity doc required
- 语言：default Python unless handout specifies

# Inputs
## Required
- lab_task: string — e.g. 实现快速排序并分析复杂度

## Optional
- language: python | java, project_path, handout

# Outputs
**Profile:** hybrid

1. `src/` implementation
2. `tests/` with cases
3. `docs/complexity.md`
4. `docs/report.md`

# Steps
1. READ refs/ds-algorithms-guide.md
2. RUN check_python.py if Python else check_java.py
3. ASK lab_task and algorithm spec; READ handout
4. IMPLEMENT with clear API; WRITE tests
5. RUN pytest or handout cases; all pass
6. WRITE docs/complexity.md — O time/space
7. DRAFT report; UPDATE checklist

# Decision
IF handout gives Java → switch toolchain
IF wrong complexity → revise before delivery
IF only paste LeetCode without local run → require local tests

# Tools
- shell, file_read, file_write, ask_user

# Failures
F1: toolchain-missing | no python/java | install
F2: test-fail | cases fail | fix algorithm
F3: missing-complexity | no O() doc | add complexity.md
F4: integrity-violation | cheat | refuse

# Deps
depends_on:
  - skill-core
  - coding-homework-assistant
provides:
  - ds-algorithm-lab

# Version
version: "1.0.0"
status: stable
